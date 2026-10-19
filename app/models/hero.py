from __future__ import annotations

from typing import Optional

from sqlmodel import Field, SQLModel


class Hero(SQLModel, table=True):
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
