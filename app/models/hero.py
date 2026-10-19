"""Table SQLModel du héros : ce qui est stocké en base SQLite."""

from sqlmodel import Field, SQLModel


class Hero(SQLModel, table=True):
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
