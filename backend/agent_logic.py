# Langgraph code

import pandas as pd
from pydantic import BaseModel, ConfigDict, Field
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END
from typing import Optional, TypedDict, List
from langchain_core.runnables import RunnableConfig
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain.tools import tool
from IPython.display import display, Markdown
from datetime import datetime
from langchain.agents import create_agent
import os
import json
from dotenv import load_dotenv
load_dotenv()

llm = HuggingFaceEndpoint(
    model="Qwen/Qwen2.5-72B-Instruct",
    task="conversational",
    huggingfacehub_api_token=os.getenv("HF_TOKEN"),
)
model = ChatHuggingFace(llm=llm)
memory = MemorySaver()
output_parser = JsonOutputParser()
format_instructions = output_parser.get_format_instructions()
chain = model | output_parser

class UserProfile(TypedDict):
    wakeup_time: str | None
    sleep_time: str | None
    profession: str | None
    class_time : str | None
    work_time : str | None
    height: float | None
    weight: float | None
    age: int | None
    priorities: list[str] | None

class Task(BaseModel):
    task: str
    start_time: str
    end_time: str
    duration: float
    task_suggestion: Optional[str] = None

class User(TypedDict):
    messages: list
    responses: list
    profile: UserProfile
    schedule: list[Task]

def user_profile_node(state: User):
    """Node function to set user profile"""
    state["profile"]["wakeup_time"] = input("At what time do you wake up? : ")
    state["profile"]["sleep_time"] = input("At what time do you sleep? : ")
    state["profile"]["profession"] = input("Enter your profession : ")

    if(state["profile"]["profession"] == "student"):
        state["profile"]["class_time"] = input("What is the time of your college/school : ")
    else:
        state["profile"]["work_time"] = input("Enter your working time : ")
    
    state["profile"]["age"] = int(input("Enter your age : "))
    state["profile"]["height"] = float(input("Enter your height : "))
    state["profile"]["weight"] = float(input("Enter your weight : "))
    state["profile"]["priorities"] = input("Select your priorities : ").split(",")
    print("User profile logged successfully.")
    return state

def detect_health(state: User):
    """Node function to detect health issues based on user profile"""
    bmi = 0.0 or None
    health_status = "" or None
    age = state["profile"]["age"]
    height = state["profile"]["height"]
    weight = state["profile"]["weight"]
    
    # Simple health risk detection based on BMI
    if weight != None and height != None:
        bmi = weight / ((height / 100) ** 2)
        if bmi < 18.5:
            health_status = "underweight"
        elif 18.5 <= bmi < 25:
            health_status = "normal weight"
        elif 25 <= bmi < 30:
            health_status = "overweight"
        else:
            health_status = "obese"
    
    state["responses"].append({"content": f"Based on your profile, your BMI is {bmi:.2f}, which is considered {health_status}."})
    return state

def create_schedule_node(state: User):
    """Creates a timetable for the user"""
    prompt = f"""
    As a professional time management expert, create a time table for the given user profile which he can follow for 21 days.
    {format_instructions}
    {state['profile']}
    
    Plan a time table for a single day according to {state} and user priorities. Make sure to reserve some time for rest.
    Keep in mind the user's health status and suggest activities according to "suggest_activities" node.
    Return all the JSON objects with this structure:
        [{{
            "task": "...",
            "start_time": "...",
            "end_time": "...",
            "duration": "...",
            "task_suggestion": "..." (optional, only if there is a suggestion for that task based on health status and priorities)
        }}]
    Always return the start_time and end_time in 12 hour format."""
    result = chain.invoke(prompt)
    print("User schedule created successfully.\n")
    print(result)
    state["schedule"] = result
    return state


def intent_parser(state: User):
    print("Understanding user intent...")
    if "messages" not in state or not state["messages"]:
        return state
    
    message = state["messages"][-1]["content"].lower()
    intent_type = "unknown"
    
    if "move" in message or "shift" in message:
        intent_type = "move"
    elif "delete" in message or "remove" in message:
        intent_type = "delete"
    elif "add" in message or "create" in message:
        intent_type = "add"
    elif "adjust" in message or "change" in message:
        intent_type = "adjust"
    
    print(f"Detected intent: {intent_type}")
    return state

def extract_task_details(state: User):
    if "messages" not in state or not state["messages"]:
        if "responses" not in state:
            state["responses"] = []
        return state
    
    message = state["messages"][-1]["content"]
    prompt = f"""Extract task modification details from user input.

Input: {message}

Return ONLY valid JSON. Do not include any explanation or text.

{{
    "task": "task name from input",
    "start_time": "desired start time",
    "end_time": "desired end time or empty if not specified",
    "duration": "duration if specified",
    "task_suggestion": "any suggestion for the task based on health status and priorities (optional)",
    "action": "move or delete or add or adjust",
    "priority": "high or low"
}}
"""
    response = chain.invoke(prompt)
    print("Message information extracted...")
    print(response)
    if "responses" not in state:
        state["responses"] = []
    state["responses"].append({"role": "system", "content": f"Extracted modification details: {response}"})
    return state

def revise_schedule_node(state: User):
    """Reschedule the previous timetable based on the extracted information"""
    # Check if responses exist and have content
    if "responses" not in state or not state["responses"]:
        print("No modification details to process")
        return state
    
    response = state["responses"][-1].get("content", "")
    schedule = state["schedule"]
    print("Comparing task within the timetable...")
    prompt = f"""You are a scheduling expert. Reschedule the user's timetable based on their modification request.

Current Schedule:
{json.dumps(schedule, indent=2)}

User Modification Request:
{response}

Task: Update ONLY the affected task in the schedule. Keep all other tasks unchanged.
- No tasks should overlap
- Preserve task duration (same as original)
- Shift subsequent tasks if needed to avoid conflicts
- Maintain task priorities

Return ONLY valid JSON array with the updated schedule. Do not include any explanation, text, or markdown.

[
    {{
        "task": "task name",
        "start_time": "HH:MM AM/PM",
        "end_time": "HH:MM AM/PM",
        "duration": "X hour(s)",
        "task_suggestion": "any suggestion for the task based on health status and priorities (optional)"
    }},
    ...
]
"""    
    result = chain.invoke(prompt)
    print(result)
    state["schedule"] = result
    return state

def schedule_tool(state: User):
    """
    Conditional routing function that determines whether to revise the schedule.
    Returns the next node name: "intent" or END
    """
    user_input = input("Enter your modification request (or press Enter to skip): ").strip()
    if user_input:
        if "messages" not in state:
            state["messages"] = []
        state["messages"].append({"role": "user", "content": user_input})
        return "intent"
    else:
        return END

SYSTEM_PROMPT = """
You are a personal assistant, which helps people with their daily routine.

Your main task is:
- schedule a time table according to the user inputs which the user can follow for 21 days.
- update or modify the timetable on the user's requests for that specific day.
- ask for the suggestions in the timtable.

If the user asks for updation or if there is some urgent task at the alloted timeslot, then shift the task to the vacant timeslot according to your understanding.
Remember to reserve some time for rest.
"""

graph = StateGraph(User)
graph.add_node("user_profile", user_profile_node)
graph.add_node("detect_health", detect_health)
graph.add_node("schedule", create_schedule_node)
graph.add_node("intent", intent_parser)
graph.add_node("extract", extract_task_details)
graph.add_node("re-schedule", revise_schedule_node)

graph.add_edge(START, "user_profile")
graph.add_edge("user_profile", "detect_health")
graph.add_edge("detect_health", "schedule")
graph.add_conditional_edges(
    "schedule",
    schedule_tool,
    {
        "intent": "intent",
        END: END
    }
)
graph.add_edge("intent", "extract")
graph.add_edge("extract", "re-schedule")
graph.add_conditional_edges(
    "re-schedule",
    schedule_tool,
    {
        "intent": "intent",
        END: END
    }
)
app = graph.compile(checkpointer=memory)
config: RunnableConfig = {"configurable": {"thread_id": "3"}}



# profile = UserProfile(
#     wakeup_time=None,
#     sleep_time=None,
#     profession= "",
#     class_time="",
#     work_time="",
#     height=0.0,
#     weight=0.0,
#     age=0,
#     priorities=[]
# )
# schedule = []
# messages = []
# responses = []

# initial_state = User(messages=messages,profile=profile,schedule=schedule,responses=responses)
# result = app.invoke(initial_state, config=config)
