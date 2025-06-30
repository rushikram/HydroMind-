from backend.db import get_history
from datetime import datetime, timedelta
from collections import defaultdict

def get_weekly_trends(user_id):
    history = get_history(user_id)
    last_7_days = defaultdict(int)

    for record in history:
        ts = record.get("timestamp")
        amount = record.get("amount_ml", 0)
        date_str = datetime.fromisoformat(ts).date().isoformat()
        if datetime.fromisoformat(ts).date() >= datetime.today().date() - timedelta(days=6):
            last_7_days[date_str] += amount

    return [{"date": date, "total_ml": last_7_days[date]} for date in sorted(last_7_days)]

def recommend_goal(user_id):
    history = get_history(user_id)
    daily_totals = defaultdict(int)

    for record in history:
        date = datetime.fromisoformat(record["timestamp"]).date()
        daily_totals[date] += record["amount_ml"]

    if not daily_totals:
        return 2000

    avg = sum(daily_totals.values()) // len(daily_totals)
    if avg < 1800:
        return 2000
    elif avg < 2200:
        return avg + 200
    else:
        return avg

def get_behavior_insights(user_id):
    history = get_history(user_id)
    hour_map = defaultdict(int)
    weekday_map = defaultdict(int)

    for record in history:
        dt = datetime.fromisoformat(record["timestamp"])
        hour_map[dt.hour] += record["amount_ml"]
        weekday_map[dt.weekday()] += record["amount_ml"]

    peak_hour = max(hour_map, key=hour_map.get, default=None)
    low_day = min(weekday_map, key=weekday_map.get, default=None)

    return {
        "most_common_drinking_hour": f"{peak_hour}:00",
        "lowest_hydration_day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][low_day]
    }
