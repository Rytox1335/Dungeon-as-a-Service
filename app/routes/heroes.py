from __future__ import annotations

import asyncio
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from app.database import get_session
from app.models.hero import Hero
from app.models.player import Player
from app.schemas.hero import HeroAttackResult, HeroCreate, HeroMove, HeroRead, HeroRoomResponse
from app.services.auth_service import decode_access_token
from app.services.dungeon_map import get_monster, get_monster_of_room, get_room
from app.services.hero_service import (
    build_hero_entity,
    ensure_hero_alive,
    ensure_hero_owner,
    ensure_monster_present,
    ensure_no_combat,
    get_hero_or_404,
    sync_monster_state,
)

router = APIRouter(prefix="/heroes", tags=["Héros"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_player(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> Player:
    try:
        payload = decode_access_token(token)
    except Exception as exc:  # pragma: no cover - garde-fou FastAPI
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "INVALID_TOKEN", "message": "Token invalide ou expiré."},
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    player_id = payload.get("sub")
    if player_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "INVALID_TOKEN", "message": "Token invalide."},
            headers={"WWW-Authenticate": "Bearer"},
        )

    player = session.get(Player, int(player_id))
    if player is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "INVALID_TOKEN", "message": "Token invalide."},
            headers={"WWW-Authenticate": "Bearer"},
        )
    return player


@router.get("", response_model=list[HeroRead])
def list_heroes(
    current_player: Player = Depends(get_current_player),
    session: Session = Depends(get_session),
) -> list[Hero]:
    return session.exec(select(Hero).where(Hero.owner_id == current_player.id)).all()


@router.post("", response_model=HeroRead, status_code=status.HTTP_201_CREATED)
def create_hero(
    payload: HeroCreate,
    current_player: Player = Depends(get_current_player),
    session: Session = Depends(get_session),
) -> Hero:
    hero = Hero(
        name=payload.name,
        classe=payload.classe,
        force=payload.force,
        agilite=payload.agilite,
        intelligence=payload.intelligence,
        pv=20 + payload.force * 2,
        room_id="entree",
        owner_id=current_player.id,
    )
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@router.get("/{id}", response_model=HeroRead)
def get_hero(
    id: int,
    current_player: Player = Depends(get_current_player),
    session: Session = Depends(get_session),
) -> Hero:
    hero = get_hero_or_404(session, id)
    ensure_hero_owner(hero, current_player)
    return hero


@router.get("/{id}/room", response_model=HeroRoomResponse)
def get_room_hero(
    id: int,
    current_player: Player = Depends(get_current_player),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    hero = get_hero_or_404(session, id)
    ensure_hero_owner(hero, current_player)
    room = get_room(hero.room_id)
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "ROOM_NOT_FOUND", "message": "Salle introuvable."},
        )
    return {
        "room_id": hero.room_id,
        "name": room["name"],
        "description": room["description"],
        "exits": room.get("exits", {}),
        "monster": room.get("monster"),
    }


@router.post("/{id}/move")
def move_hero(
    id: int,
    payload: HeroMove,
    current_player: Player = Depends(get_current_player),
    session: Session = Depends(get_session),
) -> HeroRead:
    hero = get_hero_or_404(session, id)
    ensure_hero_owner(hero, current_player)
    ensure_hero_alive(hero)

    room = get_room(hero.room_id)
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "ROOM_NOT_FOUND", "message": "Salle introuvable."},
        )
    if hero.monster_id and hero.monster_hp > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": "IN_COMBAT", "message": "Un combat est déjà en cours."},
        )
    if payload.direction not in room.get("exits", {}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "INVALID_DIRECTION", "message": "Direction invalide."},
        )

    next_room_id = room["exits"][payload.direction]
    hero.room_id = next_room_id
    sync_monster_state(hero)
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@router.post("/{id}/attack", response_model=HeroAttackResult)
def attack_hero(
    id: int,
    current_player: Player = Depends(get_current_player),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    hero = get_hero_or_404(session, id)
    ensure_hero_owner(hero, current_player)
    ensure_hero_alive(hero)

    if hero.monster_id is None or hero.monster_hp <= 0:
        room_monster = get_monster_of_room(hero.room_id)
        if room_monster is None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": "NO_MONSTER", "message": "Aucun monstre n'est présent dans cette salle."},
            )
        hero.monster_id = room_monster["id"]
        hero.monster_hp = room_monster["hp"]

    ensure_monster_present(hero)
    monster = get_monster(hero.monster_id)
    if monster is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": "NO_MONSTER", "message": "Aucun monstre n'est présent dans cette salle."},
        )

    hero_entity = build_hero_entity(hero)
    degats, critique = hero_entity.calculer_degats()
    hero.monster_hp = max(0, hero.monster_hp - degats)

    issue = "en_cours"
    degats_subis = 0
    or_gagne = 0
    victoire = False

    if hero.monster_hp <= 0:
        or_gagne = monster["gold"]
        hero.or_argent += or_gagne
        issue = "monstre_vaincu"
        if hero.room_id == "salle_trone":
            victoire = True
            hero.victoire = True
        hero.monster_id = None
        hero.monster_hp = 0
    else:
        degats_subis = hero_entity.subir_degats(monster["attack"])
        hero.pv = max(0, hero.pv - degats_subis)
        if hero.pv <= 0:
            issue = "heros_mort"

    session.add(hero)
    session.commit()
    session.refresh(hero)

    return {
        "degats_infliges": degats,
        "critique": critique,
        "degats_subis": degats_subis,
        "pv_heros": hero.pv,
        "pv_monstre": hero.monster_hp,
        "issue": issue,
        "or_gagne": or_gagne,
        "victoire": victoire,
    }


@router.post("/{id}/rest", response_model=HeroRead)
async def rest_hero(
    id: int,
    current_player: Player = Depends(get_current_player),
    session: Session = Depends(get_session),
) -> Hero:
    hero = get_hero_or_404(session, id)
    ensure_hero_owner(hero, current_player)
    ensure_hero_alive(hero)
    ensure_no_combat(hero)

    await asyncio.sleep(3)
    hero.pv = hero.pv_max
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero
