# GetClose API

Backend FastAPI du jeu de géographie **GetClose** — comptes joueurs, parties, manches, calcul de score et classement. Projet réalisé en groupe de 4 dans le cadre du module FastAPI.

## Installation

1. Créer un environnement virtuel et installer les dépendances :

   ```bash
   python -m venv venv
   source venv/bin/activate        # sous Windows : venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Démarrer PostgreSQL avec Docker :

   ```bash
   docker compose up -d
   ```

3. Copier le fichier d'exemple de configuration et l'adapter si besoin :

   ```bash
   cp .env.example .env
   ```

4. Lancer l'API en mode développement :

   ```bash
   uvicorn app.main:app --reload
   ```

5. Vérifier que ça fonctionne :
   - `http://localhost:8000/health` doit renvoyer `{"status": "ok"}`
   - `http://localhost:8000/docs` ouvre la documentation Swagger interactive

## Structure du projet

```
app/
  main.py       # crée l'app FastAPI, branche les routers
  database.py   # connexion PostgreSQL (SQLAlchemy)
  core/         # config, sécurité (hash mot de passe, JWT)
  models/       # tables SQLAlchemy, une par ressource
  schemas/      # modèles Pydantic (validation entrée/sortie)
  routers/      # routes HTTP, restent légères
  services/     # logique métier (scoring, génération de partie, geocoding)
tests/          # tests pytest, un fichier par ressource
```

## Répartition du travail

Voir le plan détaillé partagé en groupe pour la répartition des ressources, des relations et des fonctionnalités métier avancées entre les 4 membres.

## Lancer les tests

```bash
pytest
```
