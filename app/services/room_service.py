"""Logique métier du donjon : description de la salle et déplacement."""

from fastapi import HTTPException
from sqlmodel import Session

from app.models.hero import Hero
from app.schemas.room import MonsterRead, MoveRequest, RoomRead
from app.services.dungeon_map import get_monster_of_room, get_room
from app.services.hero_service import get_hero_or_404


def _erreur(status: int, code: str, message: str) -> HTTPException:
    """Construit une erreur métier au format imposé."""
    return HTTPException(status_code=status, detail={"error": code, "message": message})


def _to_room_read(hero: Hero) -> RoomRead:
    """Décrit la salle du héros ; le monstre n'apparaît que si un combat est en cours."""
    room = get_room(hero.salle_actuelle)
    monstre = None
    if hero.monstre_pv is not None:
        modele = get_monster_of_room(hero.salle_actuelle)
        monstre = MonsterRead(
            nom=modele["name"],
            pv=hero.monstre_pv,
            pv_max=modele["hp"],
            attaque=modele["attack"],
        )
    return RoomRead(
        id=hero.salle_actuelle,
        nom=room["name"],
        description=room["description"],
        sorties=list(room["exits"].keys()),
        monstre=monstre,
    )


def describe_room(session: Session, hero_id: int) -> RoomRead:
    """FT-5 : décrit la salle où se trouve le héros."""
    return _to_room_read(get_hero_or_404(session, hero_id))


def move_hero(session: Session, hero_id: int, data: MoveRequest) -> RoomRead:
    """FT-6 : déplace le héros dans la direction demandée."""
    hero = get_hero_or_404(session, hero_id)

    if hero.pv == 0:
        raise _erreur(409, "HERO_DEAD", "Le héros est mort, il ne peut plus agir.")
    if hero.monstre_pv is not None:
        raise _erreur(409, "IN_COMBAT", "Impossible de fuir : un combat est en cours.")

    destination = get_room(hero.salle_actuelle)["exits"].get(data.direction)
    if destination is None:
        raise _erreur(400, "NO_EXIT", f"Il n'y a pas de passage vers le {data.direction}.")

    hero.salle_actuelle = destination
    # Le donjon est maudit : le monstre réapparaît à chaque entrée, PV au maximum
    monstre = get_monster_of_room(destination)
    hero.monstre_pv = monstre["hp"] if monstre else None

    session.add(hero)
    session.commit()
    session.refresh(hero)
    return _to_room_read(hero)
