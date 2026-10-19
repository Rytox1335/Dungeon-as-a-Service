"""Schémas Pydantic des salles et des déplacements."""

from typing import Literal

from pydantic import BaseModel


class MonsterRead(BaseModel):
    """Monstre affronté : pv = PV actuels (hero.monstre_pv)."""

    nom: str
    pv: int
    pv_max: int
    attaque: int


class RoomRead(BaseModel):
    id: str
    nom: str
    description: str
    sorties: list[str]
    monstre: MonsterRead | None = None


class MoveRequest(BaseModel):
    """Corps de POST /heroes/{id}/move : toute autre valeur donne un 422 automatique."""

    direction: Literal["nord", "sud", "est", "ouest"]
