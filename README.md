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
    python models.py
    ```
6. Run the webserver (FastAPI and bot can be run together or as separate processes):
    ```
    uvicorn main:app --host 0.0.0.0 --port 443 --ssl-keyfile /path/to/key.pem --ssl-certfile /path/to/cert.pem
    python bot.py
    ```
7. Point your reverse proxy (nginx/Caddy) to FastAPI (port 443 or as you wish).
8. Register your webapp URL in [BotFather](https://t.me/botfather).

**Useful files:**
- `main.py` — FastAPI API + webview
- `bot.py` — aiogram Telegram bot
- `models.py` — SQLAlchemy ORM, db creation
- `templates/webapp.html` — Jinja2 template with Leaflet.js
- `static/` — contains CSS and JS (Leaflet)