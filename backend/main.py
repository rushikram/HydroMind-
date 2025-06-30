from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from backend.db import init_db, add_entry, get_history, get_today_total, reset_user_data
from backend.models import WaterEntry, ResetRequest
from agent.hydration_agent import run_agent
from backend.analysis import get_weekly_trends, recommend_goal, get_behavior_insights
from datetime import datetime
import time

# Initialize FastAPI app
app = FastAPI()

# Allow all CORS origins for simplicity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"⬅️ {request.method} {request.url}")
    response = await call_next(request)
    print(f"➡️ Status: {response.status_code}")
    return response

# Run on startup
@app.on_event("startup")
def startup_event():
    print("🔧 Initializing database...")
    init_db()

# Background reminder
def send_reminder():
    print(f"[Reminder] Time to hydrate! — {datetime.now().strftime('%H:%M:%S')}")

def schedule_reminder(delay_minutes: int = 60):
    time.sleep(delay_minutes * 60)
    send_reminder()

# ✅ Add water entry
@app.post("/add-entry/")
def add_water_entry(entry: WaterEntry, background_tasks: BackgroundTasks):
    try:
        result = add_entry(entry.user_id, entry.amount_ml)
        background_tasks.add_task(schedule_reminder, delay_minutes=60)
        return result
    except Exception as e:
        print(f"[ERROR] add_entry failed: {e}")
        return {"status": "error", "message": str(e)}

# ✅ Get hydration history
@app.get("/history/{user_id}")
def get_water_history(user_id: str):
    try:
        history = get_history(user_id)
        return history  # List of {amount_ml, timestamp}
    except Exception as e:
        print(f"[ERROR] get_history failed for {user_id}: {e}")
        return {"status": "error", "message": str(e)}

# ✅ Get today's total intake
@app.get("/today-total/{user_id}")
def get_today_total_api(user_id: str):
    try:
        total = get_today_total(user_id)
        return {"user_id": user_id, "today_total_ml": total}
    except Exception as e:
        print(f"[ERROR] get_today_total failed for {user_id}: {e}")
        return {"status": "error", "message": str(e)}

# ✅ Ask hydration AI agent
@app.post("/ask-agent/")
async def ask_agent(request: Request):
    try:
        body = await request.json()
        question = body.get("question")
        groq_key = body.get("groq_key")
        goal_ml = body.get("goal_ml", 2000)
        user_id = body.get("user_id")

        if not question or not groq_key or not user_id:
            return {"response": "Missing question, user ID, or API key."}

        response = run_agent(question, groq_key, goal_ml, user_id)
        return {"response": response}
    except Exception as e:
        print(f"[ERROR] ask-agent failed: {e}")
        return {"response": f"An error occurred: {str(e)}"}

# ✅ Reset hydration log
@app.post("/reset/")
def reset_water_log(req: ResetRequest):
    try:
        return reset_user_data(req.user_id)
    except Exception as e:
        print(f"[ERROR] reset_user_data failed: {e}")
        return {"status": "error", "message": str(e)}

# ✅ Weekly trend endpoint
@app.get("/weekly-trends/{user_id}")
def get_weekly_trends_api(user_id: str):
    try:
        return get_weekly_trends(user_id)
    except Exception as e:
        print(f"[ERROR] get_weekly_trends failed: {e}")
        return {"status": "error", "message": str(e)}

# ✅ Personalized goal endpoint
@app.get("/personal-goal/{user_id}")
def get_personal_goal(user_id: str):
    try:
        return {"recommended_goal_ml": recommend_goal(user_id)}
    except Exception as e:
        print(f"[ERROR] recommend_goal failed: {e}")
        return {"status": "error", "message": str(e)}

# ✅ Habit insight endpoint
@app.get("/habit-insights/{user_id}")
def get_behavior_insights_api(user_id: str):
    try:
        return get_behavior_insights(user_id)
    except Exception as e:
        print(f"[ERROR] get_behavior_insights failed: {e}")
        return {"status": "error", "message": str(e)}
