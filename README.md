# Dungeon as a Service — starter

Squelette fourni pour le projet bonus du module Python Backend & FastAPI.

## Installation (à faire une seule fois)

Prérequis : Python 3.10 ou plus récent (`python --version`).

```bash
# 1. Créer et activer un environnement virtuel
python -m venv .venv
# Windows (PowerShell) :
.venv\Scripts\Activate.ps1
# macOS / Linux :
source .venv/bin/activate

# 2. Installer les dépendances
pip install -r requirements.txt
```

## Lancer l'API

Depuis la racine du projet (le dossier qui contient `app/`) :

```bash
fastapi dev app/main.py
```

Ouvrez ensuite http://127.0.0.1:8000/ pour vérifier que l'API répond et trouver
les liens vers la documentation (`/docs`) et le contrôle de santé (`/health`).
La route `GET /health` doit répondre `{"status": "ok", ...}`. Si c'est le cas,
vous êtes prêts.

## Structure

```
app/
  main.py              point d'entrée, branchement des routers
  database.py          connexion SQLite (FOURNI)
  models/              tables SQLModel
  schemas/             schémas Pydantic d'entrée et de sortie
  domain/              classes métier (Heros, Guerrier, Mage, Voleur)
  services/            logique du jeu
    dungeon_map.py     lecture de la carte (FOURNI)
  routes/              routers FastAPI
data/dungeon_map.json  carte du donjon (FOURNI, ne pas modifier)
client/play.py         client terminal (BONUS)
```

## Réinitialiser la partie

Arrêtez le serveur et supprimez le fichier `dungeon.db` : il sera recréé au prochain lancement.
À faire aussi si vous ajoutez une colonne à une table (SQLite ne met pas à jour une table existante).

---

<!-- À COMPLÉTER PAR LE GROUPE AVANT LE RENDU -->

## Notre rendu

- **Membres du groupe :**
  - Laurent MASIKINI
  - Robin LAGODA
  - Yanis KATCHA
- **Lien du dépôt Git :** https://github.com/Rytox1335/Dungeon-as-a-Service.git
- **Palier atteint :** Palier 4 – Le verrou (tous les paliers sont validés). La vérification du dépôt relève toutefois l'écart signalé au palier 2 ci-dessous.

| Palier | Contenu | Statut |
|---|---|---|
| Palier 1 – Le héros | Création (`POST /heroes`), validation Pydantic, consultation (`GET /heroes`, `GET /heroes/{id}`) et erreur 404 structurée. | ✅ |
| Palier 2 – Le donjon | Persistance SQLite/SQLModel, description de la salle, déplacement et gestion d'un monstre dans une salle hantée. L'erreur de déplacement exposée est `INVALID_DIRECTION`, et non `NO_EXIT`. | ⚠️ |
| Palier 3 – Le combat | Classes métier `Heros`, `Guerrier`, `Mage` et `Voleur`, attaque, erreurs 409 pour les états empêchant d'agir et repos asynchrone. | ✅ |
| Palier 4 – Le verrou | Inscription, connexion JWT via `OAuth2PasswordRequestForm`, routes des héros protégées, erreurs 401 et 403 `NOT_YOUR_HERO`, liste filtrée par joueur. | ✅ |

- **Bonus réalisés :**
  - **B-1 Client terminal :** ⚠️ Non terminé. `client/play.py` ne propose que la sous-commande `health` (avec une réponse simulée) ; les commandes `register`, `login`, `create`, `look`, `move`, `attack` et `rest`, l'utilisation de `requests` et la sauvegarde du jeton ne sont pas implémentées.
  - **B-2 Classement :** ⚠️ Non trouvé. Aucune route `GET /leaderboard` n'est déclarée.
  - **B-3 Tests :** ⚠️ Non trouvé. Aucun fichier de tests Python ni test automatisé n'a été repéré ; le seuil d'au moins cinq tests n'est donc pas atteint.
- **Ce qui ne fonctionne pas / difficultés :**
  - Le déplacement des routes exposées renvoie `INVALID_DIRECTION` (HTTP 400) pour une direction non disponible ; il ne renvoie pas l'erreur `NO_EXIT` demandée dans le descriptif du palier 2.
  - Les modules `room_service.py` et `combat_service.py` utilisent des noms de champs (`salle_actuelle`, `monstre_pv`) différents de ceux du modèle `Hero` (`room_id`, `monster_id`, `monster_hp`) et ne sont pas utilisés par les routes actuellement branchées.
  - Le client terminal et les bonus classement et tests restent à réaliser.
