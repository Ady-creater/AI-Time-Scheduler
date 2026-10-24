// Thin client around a backend that hosts the LangGraph agent from
// agent_logic.py. The graph's LLM-driven nodes (create_schedule_node,
// extract_task_details, revise_schedule_node) need a Python process —
// this file just calls the two HTTP endpoints that backend should expose.
// See README.md for a minimal FastAPI/Flask wrapper you can drop the
// existing agent_logic.py functions into.

const BASE_URL = import.meta.env.VITE_API_BASE || "http://localhost:8000";

async function postJSON(path, body) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Request to ${path} failed (${res.status}): ${text}`);
  }
  return res.json();
}

// Mirrors create_schedule_node: send the profile + health read, get back
// the 21-day-repeatable single-day schedule as a list of task objects.
export function generateSchedule(profile, health) {
  return postJSON("/api/schedule", { profile, health });
}

// Mirrors intent_parser -> extract_task_details -> revise_schedule_node:
// send a free-text modification request plus the current schedule, get
// back the revised schedule.
export function reviseSchedule(message, schedule) {
  return postJSON("/api/modify", { message, schedule });
}
