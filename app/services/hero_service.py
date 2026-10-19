"""Logique métier des héros : création, lecture, conversion en schéma de sortie."""

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.hero import Hero
from app.schemas.hero import HeroCreate, HeroRead
from app.services.dungeon_map import START_ROOM


def get_hero_or_404(session: Session, hero_id: int) -> Hero:
    """Renvoie le héros en base, ou lève une 404 au format imposé."""
    hero = session.get(Hero, hero_id)
    if hero is None:
        raise HTTPException(
            status_code=404,
            detail={"error": "HERO_NOT_FOUND", "message": f"Le héros {hero_id} n'existe pas."},
        )
    return hero


def list_heroes(session: Session) -> list[HeroRead]:
    """Renvoie tous les héros."""
    heroes = session.exec(select(Hero)).all()
    return [to_hero_read(h) for h in heroes]


def read_hero(session: Session, hero_id: int) -> HeroRead:
    """Renvoie le détail d'un héros (même s'il est mort)."""
    return to_hero_read(get_hero_or_404(session, hero_id))


def to_hero_read(hero: Hero) -> HeroRead:
    """Convertit le modèle de table en schéma de sortie (cache monstre_pv)."""
    return HeroRead(
        id=hero.id,
        nom=hero.nom,
        classe=hero.classe,
        force=hero.force,
        agilite=hero.agilite,
        intelligence=hero.intelligence,
        pv=hero.pv,
        pv_max=hero.pv_max,
        salle_actuelle=hero.salle_actuelle,
        or_=hero.or_,
        victoire=hero.victoire,
        en_combat=hero.monstre_pv is not None,
        est_vivant=hero.pv > 0,
    )


def create_hero(session: Session, data: HeroCreate) -> HeroRead:
    """Crée un héros dans la salle de départ avec ses PV au maximum."""
    pv_max = 20 + data.force * 2
    hero = Hero(
        nom=data.nom,
        classe=data.classe,
        force=data.force,
        agilite=data.agilite,
        intelligence=data.intelligence,
        pv=pv_max,
        pv_max=pv_max,
        salle_actuelle=START_ROOM,
    )
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return to_hero_read(hero)
