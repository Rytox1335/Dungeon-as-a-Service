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
    classe: str
    force: int
    agilite: int
    intelligence: int
    pv: int
    pv_max: int
    salle_actuelle: str
    or_: int
    victoire: bool
    # Champs calculés à partir de monstre_pv et pv (fournis par le service)
    en_combat: bool
    est_vivant: bool
