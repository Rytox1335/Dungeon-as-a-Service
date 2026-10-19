from __future__ import annotations

from abc import ABC, abstractmethod
import random


class Heros(ABC):
    """Classe abstraite représentant un héros du donjon."""

    def __init__(self, force: int, agilite: int, intelligence: int) -> None:
        self.force = force
        self.agilite = agilite
        self.intelligence = intelligence

    @property
    def pv_max(self) -> int:
        return 20 + self.force * 2

    @abstractmethod
    def calculer_degats(self) -> tuple[int, bool]:
        """Renvoie les dégâts infligés et le fait que l'attaque est critique."""

    def subir_degats(self, attaque_monstre: int) -> int:
        """Dégâts réellement subis par défaut : attaque du monstre."""
        return attaque_monstre


class Guerrier(Heros):
    def calculer_degats(self) -> tuple[int, bool]:
        return 2 + self.force * 2, False

    def subir_degats(self, attaque_monstre: int) -> int:
        return max(1, attaque_monstre - 1)


class Mage(Heros):
    def calculer_degats(self) -> tuple[int, bool]:
        return 1 + self.intelligence * 3, False


class Voleur(Heros):
    def calculer_degats(self) -> tuple[int, bool]:
        degats = 2 + self.agilite * 2
        critique = random.random() < 1 / 3
        if critique:
            degats *= 2
        return degats, critique
