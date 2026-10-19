"""Point d'entrée de l'API Dungeon as a Service."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import create_db_and_tables
from app.models.hero import Hero  # noqa: F401
from app.models.player import Player  # noqa: F401
from app.routes.auth import router as auth_router
from app.routes.heroes import router as heroes_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Dungeon as a Service",
    description="Moteur de jeu de rôle textuel — Pixel Crypt",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(heroes_router)


@app.get("/health", tags=["Système"])
def health() -> dict:
    return {"status": "ok", "message": "Le donjon vous attend..."}
