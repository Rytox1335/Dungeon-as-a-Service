import asyncio
from typing import NoReturn

from fastapi import HTTPException
from sqlmodel import Session

from app.domain import creer_heros
from app.models.hero import Hero
from app.schemas.combat import AttackResult
from app.schemas.hero import HeroRead
from app.services.dungeon_map import FINAL_ROOM, get_monster_of_room
from app.services.hero_service import get_hero_or_404, to_hero_read


def _erreur(status: int, code: str, message: str) -> NoReturn:
    raise HTTPException(status_code=status, detail={"error": code, "message": message})


def _verifier_vivant(hero: Hero) -> None:
    if hero.pv == 0:
        raise HTTPException(
            status_code=409,
            detail={"error": "HERO_DEAD", "message": "Le héros est mort, il ne peut plus agir."},
        )


def _verifier_hors_combat(hero: Hero) -> None:
    if hero.monstre_pv is not None:
        raise HTTPException(
            status_code=409,
            detail={"error": "IN_COMBAT", "message": "Impossible de se reposer pendant un combat."},
        )


def attaquer(session: Session, hero_id: int) -> AttackResult:
    """Joue un tour complet et enregistre son résultat."""
    hero = get_hero_or_404(session, hero_id)
    _verifier_vivant(hero)
    if hero.monstre_pv is None:
        _erreur(409, "NO_MONSTER", "Il n'y a aucun monstre à combattre dans cette salle.")

    monstre = get_monster_of_room(hero.salle_actuelle)
    if monstre is None:
        _erreur(409, "NO_MONSTER", "Il n'y a aucun monstre à combattre dans cette salle.")

    heros_metier = creer_heros(
        hero.classe,
        hero.force,
        hero.agilite,
        hero.intelligence,
    )
    degats_infliges, critique = heros_metier.calculer_degats()
    hero.monstre_pv = max(0, hero.monstre_pv - degats_infliges)
    degats_subis = 0
    or_gagne = 0

    if hero.monstre_pv == 0:
        hero.monstre_pv = None
        or_gagne = monstre["gold"]
        hero.or_ += or_gagne
        if monstre["name"] == "La Liche" and hero.salle_actuelle == FINAL_ROOM:
            hero.victoire = True
        issue = "monstre_vaincu"
        pv_monstre = 0
    else:
        degats_subis = heros_metier.subir_degats(monstre["attack"])
        hero.pv = max(0, hero.pv - degats_subis)
        issue = "heros_mort" if hero.pv == 0 else "en_cours"
        pv_monstre = hero.monstre_pv

    session.add(hero)
    session.commit()
    session.refresh(hero)
    return AttackResult(
        degats_infliges=degats_infliges,
        critique=critique,
        degats_subis=degats_subis,
        pv_heros=hero.pv,
        pv_monstre=pv_monstre,
        issue=issue,
        or_gagne=or_gagne,
        victoire=hero.victoire,
    )


async def se_reposer(session: Session, hero_id: int) -> HeroRead:
    """Restaure les points de vie après trois secondes sans garder la session ouverte."""
    hero = get_hero_or_404(session, hero_id)
    _verifier_vivant(hero)
    _verifier_hors_combat(hero)

    session.close()
    await asyncio.sleep(3)

    hero = get_hero_or_404(session, hero_id)
    _verifier_vivant(hero)
    _verifier_hors_combat(hero)
    hero.pv = hero.pv_max
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return to_hero_read(hero)
