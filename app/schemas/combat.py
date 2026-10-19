from typing import Literal

from pydantic import BaseModel


class AttackResult(BaseModel):
    """Résultat d'un tour de combat."""

    degats_infliges: int
    critique: bool
    degats_subis: int
    pv_heros: int
    pv_monstre: int
    issue: Literal["en_cours", "monstre_vaincu", "heros_mort"]
    or_gagne: int
    victoire: bool
