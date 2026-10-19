from abc import ABC, abstractmethod
from random import randrange


class Heros(ABC):
    """Règles communes aux héros."""

    def __init__(self, force: int, agilite: int, intelligence: int) -> None:
        self.force = force
        self.agilite = agilite
        self.intelligence = intelligence

    @property
    def pv_max(self) -> int:
        return 20 + self.force * 2

    @abstractmethod
    def calculer_degats(self) -> tuple[int, bool]:
        raise NotImplementedError

    def subir_degats(self, attaque_monstre: int) -> int:
        return attaque_monstre


class Guerrier(Heros):
    """Héros robuste spécialisé dans les attaques physiques."""

    def calculer_degats(self) -> tuple[int, bool]:
        return 2 + self.force * 2, False

    def subir_degats(self, attaque_monstre: int) -> int:
        return max(1, attaque_monstre - 1)


class Mage(Heros):
    """Héros qui concentre ses dégâts sur son intelligence."""

    def calculer_degats(self) -> tuple[int, bool]:
        return 1 + self.intelligence * 3, False


class Voleur(Heros):
    """Héros rapide pouvant porter des coups critiques."""

    def calculer_degats(self) -> tuple[int, bool]:
        critique = randrange(3) == 0
        degats = 2 + self.agilite * 2
        return (degats * 2 if critique else degats), critique


_CLASSES_HEROS: dict[str, type[Heros]] = {
    "guerrier": Guerrier,
    "mage": Mage,
    "voleur": Voleur,
}


def creer_heros(classe: str, force: int, agilite: int, intelligence: int) -> Heros:
    """Construit le métier correspondant à la classe choisie."""
    classe_heros = _CLASSES_HEROS.get(classe)
    if classe_heros is None:
        raise ValueError(f"Classe de héros inconnue : {classe}")
    return classe_heros(force, agilite, intelligence)
