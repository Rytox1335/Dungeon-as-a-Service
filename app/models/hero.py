<<<<<<< HEAD
from __future__ import annotations

from typing import Optional
=======
"""Table SQLModel du héros : ce qui est stocké en base SQLite."""
>>>>>>> 539dc06e4bb68b68c8258e17dff40864c4109c31

from sqlmodel import Field, SQLModel


class Hero(SQLModel, table=True):
<<<<<<< HEAD
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    classe: str = Field(index=True)
    force: int
    agilite: int
    intelligence: int
    pv: int = 0
    room_id: str = "entree"
    or_argent: int = 0
    victoire: bool = False
    owner_id: Optional[int] = Field(default=None, foreign_key="player.id")
    monster_id: Optional[str] = Field(default=None)
    monster_hp: int = 0

    @property
    def pv_max(self) -> int:
        return 20 + self.force * 2

    @property
    def is_alive(self) -> bool:
        return self.pv > 0
=======
    id: int | None = Field(default=None, primary_key=True)
    nom: str
    classe: str
    force: int
    agilite: int
    intelligence: int
    pv: int
    pv_max: int
    salle_actuelle: str
    or_: int = 0
    # None = aucun combat en cours ; sinon PV actuels du monstre affronté
    monstre_pv: int | None = None
    victoire: bool = False
>>>>>>> 539dc06e4bb68b68c8258e17dff40864c4109c31
