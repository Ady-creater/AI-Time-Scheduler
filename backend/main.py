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
