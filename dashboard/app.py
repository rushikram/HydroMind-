import streamlit as st
import requests
import pandas as pd

# 🌐 Your FastAPI backend URL
API_BASE = "https://hydromind-8rwu.onrender.com"

st.set_page_config(page_title="HydroMind", layout="centered", page_icon="💧")
st.title("💧 HydroMind: Your AI Hydration Coach")

# Sidebar: User Preferences
st.sidebar.title("⚙️ Preferences")
user_id = st.sidebar.text_input("👤 Enter your User ID")
user_goal = st.sidebar.number_input("🥤 Set your daily goal (ml)", min_value=500, step=100, value=2000)
groq_key = st.sidebar.text_input("🔐 Groq API Key", type="password")

# 🔄 Reset hydration log
if st.sidebar.button("🔄 Reset My Log"):
    if not user_id:
        st.sidebar.warning("⚠️ Enter your User ID.")
    else:
        try:
            r = requests.post(f"{API_BASE}/reset/", json={"user_id": user_id})
            if r.status_code == 200:
                st.sidebar.success("✅ Log reset for today.")
                st.rerun()
            else:
                st.sidebar.error("❌ Failed to reset log.")
        except Exception as e:
            st.sidebar.error(f"🚫 Reset failed: {e}")

# 🚰 Water Intake Logging
st.subheader("🚰 Log Water Intake")
with st.form("log_form"):
    amount = st.number_input("Water Intake (ml)", min_value=50, step=50)
    submitted = st.form_submit_button("Add Entry")
    if submitted:
        if not user_id:
            st.warning("⚠️ Please enter your User ID.")
        else:
            try:
                response = requests.post(f"{API_BASE}/add-entry/", json={
                    "user_id": user_id,
                    "amount_ml": amount
                })
                if response.status_code == 200:
                    st.success("✅ Water logged successfully!")
                    st.rerun()
                else:
                    st.error(f"❌ Failed to log water: {response.status_code}")
            except Exception as e:
                st.error(f"🚫 Request error: {e}")

# 📊 Today's Total Intake
if user_id:
    st.subheader("📊 Today’s Total")
    try:
        res = requests.get(f"{API_BASE}/today-total/{user_id}")
        res_data = res.json()
        if res.ok and "today_total_ml" in res_data:
            total = res_data["today_total_ml"]
            st.metric(label="💧 Total Today", value=f"{total} ml", delta=f"{user_goal - total} ml left")
        else:
            st.warning(f"⚠️ Could not fetch total intake. Server said: {res_data.get('message', 'Unknown error')}")
    except Exception as e:
        st.warning(f"⚠️ Error fetching total: {e}")

# 📈 Hydration History (All-Time)
st.subheader("📈 Hydration History")
if not user_id:
    st.info("👤 Enter your User ID to view history.")
else:
    try:
        response = requests.get(f"{API_BASE}/history/{user_id}")
        data_json = response.json()
        if response.ok and isinstance(data_json, list):
            if len(data_json) > 0:
                data = pd.DataFrame(data_json)
                data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
                st.line_chart(data.set_index("timestamp")["amount_ml"])
            else:
                st.info("📭 No hydration entries yet.")
        else:
            st.warning("⚠️ Unexpected data format received.")
    except Exception as e:
        st.error(f"🚫 Error loading history: {e}")

# 🤖 Ask AI Hydration Coach
st.subheader("🤖 Ask Your Hydration Coach")
question = st.text_input("Ask something like: 'Did I drink enough today?'")
if st.button("Ask"):
    if not groq_key or not question or not user_id:
        st.warning("⚠️ Please enter your User ID, API key, and a question.")
    else:
        try:
            full_prompt = f"{question.strip()} (Today’s hydration goal: {user_goal} ml)"
            response = requests.post(
                f"{API_BASE}/ask-agent/",
                json={
                    "question": full_prompt,
                    "groq_key": groq_key,
                    "goal_ml": user_goal,
                    "user_id": user_id
                }
            )
            if response.ok:
                st.markdown(f"**🧠 Coach says:** {response.json().get('response')}")
            else:
                st.error(f"❌ Agent error: {response.status_code}")
        except Exception as e:
            st.error(f"🚫 Agent request failed: {e}")

# 📆 Weekly Trend Analysis
st.subheader("📆 Weekly Hydration Trend")
if user_id:
    try:
        response = requests.get(f"{API_BASE}/weekly-trends/{user_id}")
        trend_data = response.json()
        if response.ok and isinstance(trend_data, list) and len(trend_data) > 0:
            df_trend = pd.DataFrame(trend_data)
            df_trend["date"] = pd.to_datetime(df_trend["date"])
            df_trend = df_trend.sort_values("date")
            st.line_chart(df_trend.set_index("date")["total_ml"])
        else:
            st.info("📭 No trend data yet. Log water across days to see trends.")
    except Exception as e:
        st.error(f"🚫 Trend data fetch failed: {e}")

# 🎯 Personalized Goal Suggestion
st.subheader("🎯 Personalized Goal")
if user_id:
    try:
        response = requests.get(f"{API_BASE}/personal-goal/{user_id}")
        if response.ok:
            suggested_goal = response.json().get("recommended_goal_ml", 2000)
            st.success(f"🔍 Based on your history, your personalized goal is **{suggested_goal} ml**.")
        else:
            st.warning("⚠️ Could not fetch personalized goal.")
    except Exception as e:
        st.error(f"🚫 Failed to fetch goal suggestion: {e}")

# 🧠 Habit Insights
st.subheader("🧠 Hydration Habits")
if user_id:
    try:
        response = requests.get(f"{API_BASE}/habit-insights/{user_id}")
        insights = response.json()
        if response.ok:
            st.info(f"💡 You drink most often around **{insights['most_common_drinking_hour']}**.")
            st.info(f"📉 You hydrate the least on **{insights['lowest_hydration_day']}**.")
        else:
            st.warning("⚠️ Could not fetch habit insights.")
    except Exception as e:
        st.error(f"🚫 Failed to get behavior insights: {e}")
