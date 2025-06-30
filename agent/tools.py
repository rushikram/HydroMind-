from langchain.agents import Tool
from backend.db import get_today_total
from backend.analysis import get_weekly_trends, recommend_goal, get_behavior_insights

def get_tools(goal_ml: int, user_id: str):
    # Tool 1: Today's intake vs goal
    def water_intake_history_tool(_: str) -> str:
        try:
            total = get_today_total(user_id)
            if total >= goal_ml:
                return f"🎉 You've met your hydration goal of {goal_ml} ml! Total intake: {total} ml."
            else:
                remaining = goal_ml - total
                return f"💧 You've consumed {total} ml today. {remaining} ml left to reach your goal of {goal_ml} ml."
        except Exception as e:
            return f"⚠️ Error retrieving water intake: {str(e)}"

    # Tool 2: Static goal reminder
    def hydration_goal_tool(_: str) -> str:
        return f"📌 Your current hydration goal is {goal_ml} ml per day."

    # Tool 3: Weekly trend
    def weekly_trends_tool(_: str) -> str:
        try:
            trends = get_weekly_trends(user_id)
            return f"📆 Weekly Trend:\n" + "\n".join([f"{d['date']}: {d['total_ml']} ml" for d in trends])
        except Exception as e:
            return f"⚠️ Error fetching trends: {str(e)}"

    # Tool 4: Personalized goal suggestion
    def personalized_goal_tool(_: str) -> str:
        try:
            suggested = recommend_goal(user_id)
            return f"🎯 Based on your intake history, a recommended daily goal is {suggested} ml."
        except Exception as e:
            return f"⚠️ Could not fetch personalized goal: {str(e)}"

    # Tool 5: Habit insight
    def habit_insights_tool(_: str) -> str:
        try:
            insights = get_behavior_insights(user_id)
            return (
                f"🧠 Habit Insights:\n"
                f"- Most frequent drinking time: {insights['most_common_drinking_hour']}\n"
                f"- Least hydrated day: {insights['lowest_hydration_day']}"
            )
        except Exception as e:
            return f"⚠️ Could not fetch habit insights: {str(e)}"

    # Return all tools
    return [
        Tool.from_function(
            name="Water Intake History",
            func=water_intake_history_tool,
            description="Returns today's water intake. Input can be anything."
        ),
        Tool.from_function(
            name="Hydration Goal",
            func=hydration_goal_tool,
            description="Returns the user’s static hydration goal (ml). Input can be anything."
        ),
        Tool.from_function(
            name="Weekly Trends",
            func=weekly_trends_tool,
            description="Returns hydration totals for the past 7 days. Input can be anything."
        ),
        Tool.from_function(
            name="Personalized Goal Suggestion",
            func=personalized_goal_tool,
            description="Suggests a personalized hydration goal based on user's intake history. Input can be anything."
        ),
        Tool.from_function(
            name="Hydration Habit Insights",
            func=habit_insights_tool,
            description="Returns user's most common hydration hour and lowest hydration day. Input can be anything."
        )
    ]
