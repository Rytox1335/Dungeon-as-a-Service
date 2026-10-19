from __future__ import annotations

from typing import Any

from fastapi import HTTPException
from sqlmodel import Session

from app.domain.heros import Guerrier, Heros, Mage, Voleur
from app.models.hero import Hero
from app.models.player import Player
from app.services.dungeon_map import get_monster, get_monster_of_room, get_room


def build_hero_entity(hero: Hero) -> Heros:
    if hero.classe == "guerrier":
        return Guerrier(hero.force, hero.agilite, hero.intelligence)
    if hero.classe == "mage":
        return Mage(hero.force, hero.agilite, hero.intelligence)
    if hero.classe == "voleur":
        return Voleur(hero.force, hero.agilite, hero.intelligence)
    raise ValueError(f"Classe de héros inconnue : {hero.classe}")


def get_hero_or_404(session: Session, hero_id: int) -> Hero:
    hero = session.get(Hero, hero_id)
    if hero is None:
        raise HTTPException(
            status_code=404,
            detail={"error": "HERO_NOT_FOUND", "message": "Héros introuvable."},
        )
    return hero


def ensure_hero_owner(hero: Hero, player: Player) -> None:
    if hero.owner_id != player.id:
        raise HTTPException(
            status_code=403,
            detail={"error": "NOT_YOUR_HERO", "message": "Ce héros ne vous appartient pas."},
        )


def ensure_hero_alive(hero: Hero) -> None:
    if hero.pv <= 0:
        raise HTTPException(
            status_code=409,
            detail={"error": "HERO_DEAD", "message": "Ce héros est mort et ne peut plus agir."},
        )


def ensure_no_combat(hero: Hero) -> None:
    if hero.monster_id and hero.monster_hp > 0:
        raise HTTPException(
            status_code=409,
            detail={"error": "IN_COMBAT", "message": "Un combat est déjà en cours."},
        )


def ensure_monster_present(hero: Hero) -> None:
    if hero.monster_id is None or hero.monster_hp <= 0:
        raise HTTPException(
            status_code=409,
            detail={"error": "NO_MONSTER", "message": "Aucun monstre n'est présent dans cette salle."},
        )


def sync_monster_state(hero: Hero) -> None:
    room = get_room(hero.room_id)
    room_monster_id = room.get("monster") if room else None
    if room_monster_id is None:
        hero.monster_id = None
        hero.monster_hp = 0
        return

    monster = get_monster(room_monster_id)
    if monster is None:
        hero.monster_id = None
        hero.monster_hp = 0
        return

    hero.monster_id = room_monster_id
    hero.monster_hp = monster["hp"]


def get_room_state(room_id: str) -> dict[str, Any] | None:
    room = get_room(room_id)
    if room is None:
        return None
    return {
        "room_id": room_id,
        "name": room["name"],
        "description": room["description"],
        "exits": room.get("exits", {}),
        "monster": room.get("monster"),
    }


def get_monster_state_for_room(room_id: str) -> dict[str, Any] | None:
    room = get_room(room_id)
    if room is None or room.get("monster") is None:
        return None
    monster_id = room["monster"]
    monster = get_monster(monster_id)
    if monster is None:
        return None
    return {"id": monster_id, **monster}


def get_active_monster(hero: Hero) -> dict[str, Any] | None:
    if hero.monster_id is not None:
        monster = get_monster(hero.monster_id)
        if monster is not None:
            return {"id": hero.monster_id, **monster}
    return get_monster_of_room(hero.room_id)
