# Daybook — AI Time Scheduler

Daybook is a work-in-progress daily-planning app. A React interface collects a
user's routine and priorities, displays a health summary, requests a suggested
daily schedule, and lets the user ask for schedule changes in plain language.
The Python backend uses LangChain/LangGraph and a Hugging Face-hosted language
model to generate and revise schedules.

## Project structure

```text
backend/
  agent_logic.py   LangGraph nodes and LLM prompts
  main.py          FastAPI endpoints for schedule generation and revision
  auth.py          Authentication helpers
  config.py        Application settings
  database.py      Database connection setup
  models.py        Database models
  schemas.py       Request/response schemas
frontend/
  src/             React app, profile form, health summary, and schedule UI
  package.json     Vite scripts and frontend dependencies
requirements.txt   Python dependencies
```

## Requirements

- Python 3.10 or later
- Node.js and npm
- A Hugging Face access token with access to the configured model

Some backend runtime packages used by the API are not currently listed in
`requirements.txt`. Install the project dependencies and those packages with:

```bash
python -m pip install -r requirements.txt fastapi uvicorn langchain-huggingface
```

## Configuration

Create `backend/.env` and set the model credential:

```dotenv
HF_TOKEN=your_hugging_face_token
```

Keep credentials out of source control. The backend loads this file when
started with `backend/` as its working directory.

## Run locally

Start the backend in one terminal:

```bash
cd backend
python -m uvicorn main:api --reload --port 8000
```

Start the frontend in another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend defaults to `http://localhost:8000`. To use another backend URL,
set `VITE_API_BASE` in the frontend environment, for example:

```dotenv
VITE_API_BASE=http://localhost:8000
```

The backend exposes `POST /api/schedule` and `POST /api/modify`. The API
currently returns the generated or revised schedule directly as a JSON array.

## Current limitations

- Schedules are generated for one day and intended to be repeatable for 21 days;
  the app does not currently persist a 21-day calendar.
- Health status is calculated in the frontend and shown as guidance, not as a
  medical diagnosis.
- The agent's prompt and API behavior are evolving; some older interactive
  graph functions still use terminal input and are not used by the HTTP
  endpoints.
