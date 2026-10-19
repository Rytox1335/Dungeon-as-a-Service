"""Point d'entrée de l'API Dungeon as a Service."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import create_db_and_tables
<<<<<<< HEAD
from app.models.hero import Hero  # noqa: F401
from app.models.player import Player  # noqa: F401
from app.routes.auth import router as auth_router
from app.routes.heroes import router as heroes_router
=======

# Import du modèle pour que SQLModel crée la table au démarrage
from app.models.hero import Hero  # noqa: F401
from app.routes import heroes
>>>>>>> 539dc06e4bb68b68c8258e17dff40864c4109c31


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

<<<<<<< HEAD
app.include_router(auth_router)
app.include_router(heroes_router)
=======
app.include_router(heroes.router)


@app.get("/", tags=["Système"])
def index() -> dict[str, str]:
    """Présente l'API et ses points d'entrée principaux."""
    return {
        "name": "Dungeon as a Service",
        "message": "Le donjon vous attend...",
        "docs": "/docs",
        "health": "/health",
    }
>>>>>>> 539dc06e4bb68b68c8258e17dff40864c4109c31


@app.get("/health", tags=["Système"])
def health() -> dict:
    return {"status": "ok", "message": "Le donjon vous attend..."}
