# Invevent Telegram Mini Web App (MVP)

**Features:**  
- Telegram bot (aiogram) to create, join, list, and manage events and friends  
- Webview (FastAPI) for interactive event map (Leaflet.js)
- SQLite database

**Setup:**

1. Install Python 3.11+, pip, and virtualenv.
2. Create and activate virtualenv:
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
4. Copy `.env.example` to `.env` and set your variables.
5. Run DB migrations:
    ```
    python -m invevent.models
    ```
6. Run the webserver (FastAPI and bot can be run together or as separate processes):
    ```
    uvicorn invevent.web.main:app --host 0.0.0.0 --port 443 --ssl-keyfile /path/to/key.pem --ssl-certfile /path/to/cert.pem
    python -m invevent.bot
    ```
7. Point your reverse proxy (nginx/Caddy) to FastAPI (port 443 or as you wish).
8. Register your webapp URL in [BotFather](https://t.me/botfather).

**Useful files:**
- `invevent/web/main.py`  FastAPI API + webview
- `invevent/bot/main.py`  aiogram Telegram bot
- `invevent/models.py`  SQLAlchemy ORM, db creation
- `templates/webapp.html`  Jinja2 template with Leaflet.js
- `static/`  contains CSS and JS (Leaflet)

## Deploying to a VPS

The repository includes a workflow `.github/workflows/deploy.yml` that deploys
the latest commit to your server.  The workflow connects to your VPS via SSH,
pulls the repository, removes `db.sqlite`, and restarts the systemd services
`invevent-api` and `invevent-bot`.

### Setup

1. On your VPS clone this repository and create two systemd services named
   `invevent-api` and `invevent-bot` that start the FastAPI app and the bot.
2. Add the following repository secrets on GitHub:
   - `VPS_HOST` – server hostname or IP.
   - `VPS_USER` – SSH user.
   - `VPS_KEY` – private SSH key for the user.
   - `VPS_PATH` – path to the project directory on the server.
   - `VPS_PORT` – SSH port (optional, defaults to 22).
3. Push to the `main` branch to trigger the workflow and deploy.

