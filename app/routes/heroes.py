"""Routes HTTP des héros : uniquement la couche HTTP, la logique est dans les services."""

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.schemas.hero import HeroCreate, HeroRead
from app.schemas.room import MoveRequest, RoomRead
from app.services import hero_service, room_service

router = APIRouter(prefix="/heroes", tags=["heroes"])


@router.post("", response_model=HeroRead, status_code=201)
def create_hero(data: HeroCreate, session: Session = Depends(get_session)):
    """Crée un héros (FT-1)."""
    return hero_service.create_hero(session, data)


@router.get("", response_model=list[HeroRead], status_code=200)
def list_heroes(session: Session = Depends(get_session)):
    """Liste tous les héros (FT-3)."""
    return hero_service.list_heroes(session)


@router.get("/{hero_id}", response_model=HeroRead, status_code=200)
def get_hero(hero_id: int, session: Session = Depends(get_session)):
    """Détail d'un héros (FT-3)."""
    return hero_service.read_hero(session, hero_id)


@router.get("/{hero_id}/room", response_model=RoomRead, status_code=200)
def get_hero_room(hero_id: int, session: Session = Depends(get_session)):
    """Décrit la salle du héros (FT-5)."""
    return room_service.describe_room(session, hero_id)


@router.post("/{hero_id}/move", response_model=RoomRead, status_code=200)
def move_hero(hero_id: int, data: MoveRequest, session: Session = Depends(get_session)):
    """Déplace le héros et renvoie la nouvelle salle (FT-6)."""
    return room_service.move_hero(session, hero_id, data)
