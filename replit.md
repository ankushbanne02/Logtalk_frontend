# LogTalk Frontend

## Overview
A Dash (Python/Flask) web frontend for the LogTalk system. Provides login, password reset, a chatbot interface, and a database collections view. Talks to a separate backend service via the `BACKEND_URI` environment variable.

## Tech Stack
- Python 3.12
- Dash + dash-bootstrap-components (Flask under the hood)
- Plotly, Pandas, NumPy
- LangChain / LangGraph / OpenAI client
- MongoDB client (pymongo), Azure Key Vault SDK

## Project Structure
- `chatbot_app.py` — App entry point, routing, navbar, top-level callbacks
- `chatbot_frontend.py` — Chatbot layout and callbacks
- `layouts/` — Page layouts (`login.py`, `database.py`, `reset_password.py`)
- `callbacks/` — Page callbacks (login, database, reset password)
- `assets/` — CSS, fonts, images served by Dash
- `standard_config.py` — Shared maps (state codes, colors, sort codes)
- `requirements.txt` — Python dependencies
- `Dockerfile` — Reference container build (not used on Replit)

## Replit Setup
- Workflow `Start application` runs `python chatbot_app.py` and waits for port 5000.
- App binds to `0.0.0.0:5000` so the Replit preview proxy can reach it.
- Deployment target: `autoscale`, running `gunicorn --bind=0.0.0.0:5000 --reuse-port chatbot_app:server`.

## Configuration
- `BACKEND_URI` — Base URL of the LogTalk backend API. Login, database, chatbot, and reset-password callbacks all call this. Must be set as a Replit secret for those flows to work; without it the UI loads but backend-dependent actions will fail.
