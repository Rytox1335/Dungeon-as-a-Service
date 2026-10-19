from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.database import get_session
from app.models.player import Player
from app.schemas.player import PlayerCreate, PlayerRead, Token
from app.services.auth_service import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Authentification"])


@router.post("/register", response_model=PlayerRead, status_code=status.HTTP_201_CREATED)
def register_player(
    payload: PlayerCreate,
    session: Session = Depends(get_session),
) -> Player:
    existing = session.exec(select(Player).where(Player.username == payload.username)).first()
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": "USERNAME_TAKEN", "message": "Ce nom d'utilisateur est déjà utilisé."},
        )

    player = Player(
        username=payload.username,
        password_hash=hash_password(payload.password),
    )
    session.add(player)
    session.commit()
    session.refresh(player)
    return player


@router.post("/login", response_model=Token)
def login_player(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
) -> Token:
    player = session.exec(select(Player).where(Player.username == form_data.username)).first()
    if player is None or not verify_password(form_data.password, player.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "INVALID_CREDENTIALS", "message": "Identifiants incorrects."},
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(player.id)
    return Token(access_token=access_token)
