# Daybook — frontend for the scheduling agent

A small React (Vite) app that gives `agent_logic.py`'s LangGraph a UI:

1. **Profile** — replaces the `input()` calls in `user_profile_node`.
2. **Health read** — BMI/status is computed client-side with the same
   thresholds as `detect_health`, so it appears instantly.
3. **Schedule** — calls your backend, which should run
   `create_schedule_node`'s prompt through the LLM and return the result.
4. **Modify** — a text box that replaces the `input()` loop in
   `schedule_tool`; it sends free-text requests ("move my workout to 6pm")
   to your backend, which should run `intent_parser` → `extract_task_details`
   → `revise_schedule_node`.

## Run it

```bash
cd frontend
npm install
npm run dev
```

By default it calls a backend at `http://localhost:8000`. Point it elsewhere
with an env var:

```bash
VITE_API_BASE=https://your-api.example.com npm run dev
```

## Backend contract

`agent_logic.py` as written drives its graph with blocking `input()` calls
and a `MemorySaver` checkpointer — neither works behind an HTTP request. To
use it from this frontend, wrap the same node functions in two endpoints:

- `POST /api/schedule` — body `{ profile, health }`, returns the schedule
  array (what `create_schedule_node` produces).
- `POST /api/modify` — body `{ message, schedule }`, returns the *updated*
  schedule array (what `revise_schedule_node` produces after
  `intent_parser` → `extract_task_details`).

A minimal FastAPI wrapper around your existing functions:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent_logic import create_schedule_node, revise_schedule_node

api = FastAPI()
api.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@api.post("/api/schedule")
def schedule(body: dict):
    state = {"profile": body["profile"], "responses": [], "messages": [], "schedule": []}
    state = create_schedule_node(state)
    return state["schedule"]

@api.post("/api/modify")
def modify(body: dict):
    state = {
        "schedule": body["schedule"],
        "responses": [{"role": "system", "content": body["message"]}],
        "messages": [{"role": "user", "content": body["message"]}],
        "profile": {},
    }
    state = revise_schedule_node(state)
    return state["schedule"]
```

Run it with `uvicorn server:api --reload --port 8000` alongside `npm run dev`.

## Structure

```
frontend/
  src/
    App.jsx              orchestrates profile -> health -> schedule -> modify
    health.js             client-side BMI calc (mirrors detect_health)
    api.js                 fetch wrappers for /api/schedule and /api/modify
    components/
      ProfileForm.jsx      inputs from user_profile_node
      HealthCard.jsx       BMI + status readout
      ScheduleTimeline.jsx vertical timeline of Task objects
      ModifyBar.jsx        free-text modification input
```
