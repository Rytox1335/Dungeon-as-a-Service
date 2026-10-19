<<<<<<< HEAD
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class HeroCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    classe: Literal["guerrier", "mage", "voleur"]
    force: int = Field(ge=1, le=20)
    agilite: int = Field(ge=1, le=20)
    intelligence: int = Field(ge=1, le=20)


class HeroRead(BaseModel):
    id: int
    name: str
=======
"""Schémas Pydantic des héros (entrée et sortie)."""

from typing import Literal

from pydantic import BaseModel, Field, model_validator


class HeroCreate(BaseModel):
    """Corps de la requête POST /heroes."""

    nom: str = Field(min_length=3, max_length=20)
    classe: Literal["guerrier", "mage", "voleur"]
    force: int = Field(ge=1, le=8)
    agilite: int = Field(ge=1, le=8)
    intelligence: int = Field(ge=1, le=8)

    @model_validator(mode="after")
    def verifier_somme_stats(self):
        # Le ValueError est transformé en erreur 422 par FastAPI
        if self.force + self.agilite + self.intelligence != 10:
            raise ValueError("La somme force + agilite + intelligence doit valoir 10")
        return self


class HeroRead(BaseModel):
    """Réponse de l'API : monstre_pv n'est jamais exposé tel quel."""

    id: int
    nom: str
>>>>>>> 539dc06e4bb68b68c8258e17dff40864c4109c31
    classe: str
    force: int
    agilite: int
    intelligence: int
    pv: int
    pv_max: int
<<<<<<< HEAD
    room_id: str
    or_argent: int
    victoire: bool
    monster_id: str | None = None
    monster_hp: int = 0

    model_config = {"from_attributes": True}


class HeroMove(BaseModel):
    direction: str = Field(min_length=1, max_length=20)


class HeroAttackResult(BaseModel):
    degats_infliges: int
    critique: bool
    degats_subis: int
    pv_heros: int
    pv_monstre: int
    issue: str
    or_gagne: int
    victoire: bool


class HeroRoomResponse(BaseModel):
    room_id: str
    name: str
    description: str
    exits: dict[str, str]
    monster: str | None = None
=======
    salle_actuelle: str
    or_: int
    victoire: bool
    # Champs calculés à partir de monstre_pv et pv (fournis par le service)
    en_combat: bool
    est_vivant: bool
>>>>>>> 539dc06e4bb68b68c8258e17dff40864c4109c31
