# Monitoring Agent

Supervision de serveurs en deux parties :

- **[agent](agent/)** : un service FastAPI à installer sur chaque serveur à surveiller. Il collecte les métriques CPU, RAM, disque et logs, et les expose via une API REST.
- **[web-ui](web-ui/)** : un dashboard Dash qui interroge un ou plusieurs agents et affiche leurs métriques en temps réel, avec des graphiques d'historique.

## Structure du repo

```
.
├── agent/     # API de métriques (FastAPI + psutil)
└── web-ui/    # dashboard (Dash + Plotly)
```

Chaque dossier est un projet Python autonome, avec son propre `Dockerfile`, `Makefile`, ses dépendances et ses tests.

## Démarrage rapide avec Docker

```bash
# Construire les images
docker build -t monitoring-agent ./agent
docker build -t monitoring-web-ui ./web-ui

# Lancer les conteneurs
docker run -d --name mon-agent -p 8000:8000 monitoring-agent
docker run -d --name mon-webui -p 8050:8050 monitoring-web-ui
```

- Dashboard : http://localhost:8050
- Documentation de l'API de l'agent : http://localhost:8000/docs

Pour ajouter l'agent local dans le dashboard, saisir **`host.docker.internal:8000`**. Dans le conteneur web-ui, `localhost` désigne le conteneur lui-même, pas la machine. Pour un serveur distant, saisir `<ip-du-serveur>:8000`.

Pour tout arrêter :

```bash
docker rm -f mon-agent mon-webui
```

> Quand l'agent tourne dans un conteneur, les métriques qu'il remonte concernent le conteneur, pas la machine hôte.

## Développement en local

Nécessite Python 3.11 ou plus.

**Agent**

```bash
cd agent
make environment          # crée .venv et installe les dépendances de dev
source .venv/bin/activate
make debug                # mode local avec rechargement auto, API sur :8000
```

**Web UI**

```bash
cd web-ui
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.dev.txt
python src/app.py         # dashboard sur :8050
```

## Tests et qualité

À lancer depuis `agent/` ou `web-ui/`, avec les dépendances de dev installées :

```bash
make coverage-test        # pytest + couverture (échoue sous 80 %)
ruff check src/           # lint
make find-security-issues # bandit
```

## API de l'agent

| Groupe | Routes |
|---|---|
| Général | `/health`, `/version`, `/hostname` |
| CPU | `/metrics/v1/cpu/`, `name`, `frequency`, `usage`, `core`, `averageuse` |
| RAM | `/metrics/v1/ram/total`, `free`, `used`, `percent` |
| Disque | `/metrics/v1/disk/`, `usage`, `total`, `free`, `used`, `percent` |
| Logs | `/metrics/v1/logs/usage`, `topprocesses`, `error_count`, `last_errors`, `most_viewed_page` |

La documentation interactive complète est disponible sur `/docs` (Swagger) ou `/redoc`.

Les métriques de logs sont lues dans le log d'accès Apache (`/var/log/apache2/other_vhosts_access.log`). Si ce fichier n'existe pas, ces routes renvoient des données vides.

### Configuration (variables d'environnement)

| Variable | Défaut | Description |
|---|---|---|
| `AGENT_ENV` | `production` | `local` active le rechargement automatique |
| `AGENT_VERSION` | `1.0.0` | Renvoyée par `/version` |
| `AGENT_DESCRIPTION` | `api for python agent` | Affichée dans la doc de l'API |
| `AGENT_DEBUG` | `False` | Mode debug |

Exemple : `docker run -e AGENT_VERSION=1.2.0 -p 8000:8000 monitoring-agent`
