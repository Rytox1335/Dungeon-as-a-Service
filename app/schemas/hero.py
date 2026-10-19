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
    classe: str
    force: int
    agilite: int
    intelligence: int
    pv: int
    pv_max: int
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
