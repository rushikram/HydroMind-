# 💧 HydroMind – Your AI-Powered Hydration Coach

<div align="center">

![LangChain](https://img.shields.io/badge/LangChain-Powered-green?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-AI-purple?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-teal?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red?style=for-the-badge)

**Agentic AI-powered hydration tracking system with intelligent coaching and personalized insights**

[🌐 Live Demo](#-live-deployment) • [🚀 Quick Start](#-quick-start) • [🤖 AI Features](#-ai-features) • [🏗️ Architecture](#️-technical-architecture)

</div>

---

## 📋 Project Overview

HydroMind is an **agentic AI–powered hydration tracking system** that leverages **LangChain agents** and **Groq's ultra-fast LLMs** to deliver personalized, real-time hydration coaching. Unlike traditional static apps, HydroMind acts as an autonomous AI agent that perceives user behavior, reasons over their hydration data, and proactively responds with tailored suggestions and actionable feedback.

### 🎯 **Key Problem Solved**
- Manual water intake tracking is tedious and often forgotten
- Generic hydration advice doesn't account for individual patterns and needs
- No intelligent feedback system for analyzing hydration habits
- Lack of personalized coaching based on user behavior

### 💡 **Solution Approach**
- **LangChain agents** with custom tools for dynamic data retrieval and analysis
- **Groq AI** for lightning-fast, personalized hydration coaching
- **Multi-user support** with individual tracking, goals, and insights
- **Visual analytics** for trend analysis and pattern recognition

---

## 🏗️ Technical Architecture of Agentic-AI

```
User Request → LangChain Agent → Custom Tools → Database → AI Response
                     ↓
               Groq LLM (Fast Inference)
                     ↓
            Streamlit UI ← FastAPI Backend
```

### **Core Components:**

| Component | Technology | Purpose |
|-----------|------------|---------|
| **AI Agent** | LangChain | Orchestrates tools and generates intelligent responses |
| **LLM Provider** | Groq (LLaMA3-70B) | Ultra-fast AI inference for coaching |
| **Custom Tools** | Python Functions | Fetch user data, calculate goals, analyze patterns |
| **Database** | SQLite | Store user intake data with timestamps |
| **API Backend** | FastAPI | RESTful service with comprehensive endpoints |
| **Frontend** | Streamlit | Interactive user interface with visualizations |
| **Analytics** | Pandas | Data processing and trend analysis |

---

## 🌟 Key Features

### **💧 Smart Hydration Tracking**
- Log daily water intake in milliliters with precise timestamps
- Automatic daily totals and comprehensive hydration history
- Multi-user support with individual user profiles

### **📊 Intelligent Analytics**
- Interactive weekly hydration trend visualizations
- Peak hydration time analysis (discover your optimal drinking hours)
- Day-of-week patterns (identify your least hydrated days)
- Progress tracking against personalized goals

### **🤖 AI-Powered Coaching**
- Natural language queries to your personal hydration coach
- Real-time feedback based on current intake levels
- Personalized hydration goals generated from your patterns
- Contextual advice and actionable recommendations

### **🔧 Advanced Features**
- Optional hydration log reset functionality
- Comprehensive API documentation
- Scalable multi-user architecture
- Real-time data synchronization

---

## 🗂️ Project Structure

```
hydromind/
├── app.py                   # Streamlit frontend application
├── tools.py                 # LangChain custom tools definition
├── backend/
│   ├── main.py             # FastAPI application
│   ├── db.py               # Database operations & analytics
│   ├── models.py           # Pydantic data models
│   └── analysis.py         # Trend analysis & insights engine
├── agent/
│   └── hydration_agent.py  # LangChain + Groq AI logic
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

---

## ⚡ Quick Start

### 1. **Clone Repository**
```bash
git clone https://github.com/yourusername/hydromind.git
cd hydromind
```

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Setup Groq API Key**
```bash
# Get your free API key from: https://console.groq.com/keys
export GROQ_API_KEY="your_api_key_here"
```

### 4. **Launch Backend**
```bash
uvicorn backend.main:app --reload
```

### 5. **Start Frontend**
```bash
streamlit run app.py
```

### 6. **Access Application**
- **Frontend**: `http://localhost:8501`
- **API Docs**: `http://localhost:8000/docs`

---

## 🤖 AI Features

### **LangChain Agent Capabilities:**

✅ **Smart Data Retrieval**
- Fetches real-time user water intake using custom tools
- Calculates progress against personalized hydration goals
- Analyzes historical patterns and trends

✅ **Intelligent Coaching**
- Provides contextual advice based on current intake and patterns
- Suggests optimal drinking schedules and amounts
- Identifies improvement opportunities

✅ **Multi-User Intelligence**
- Handles multiple users with dynamic `user_id` parameter
- Maintains separate tracking and personalized insights for each user
- Learns from individual behavior patterns

### **Example AI Interactions:**

```
🤖 User: "How am I doing with my hydration today?"
💧 AI: "You've consumed 1.2L out of your 2.5L daily goal (48% complete). 
       Based on your patterns, you typically drink most water around 17:00. 
       I recommend having 300ml now and setting reminders for every 2 hours."

🤖 User: "What are my hydration patterns?"
💧 AI: "You drink most water around 17:00 and hydrate least on Mondays. 
       Your weekly average is 2.1L. Consider setting Monday reminders 
       to improve consistency!"
```

---

## 🌐 Live Deployment

| Service | URL | Status |
|---------|-----|--------|
| **Frontend App** | [Streamlit-https://a6ctmbcau998klqqghwnjx.streamlit.app/](https://a6ctmbcau998klqqghwnjx.streamlit.app/) |🟢 Live |
| **API Backend** | [Render-https://hydromind-8rwu.onrender.com](https://hydromind-8rwu.onrender.com) | 🟢 Live |
| **Documentation** | [GitHub Repository](https://github.com/yourusername/hydromind) | 🟢 Active |

> 💡 **Try it out**: Use any test `user_id` like `testuser` to simulate hydration entries

---

## 🔧 Technical Implementation

### **Custom LangChain Tools:**

```python
@tool
def get_user_hydration_data(user_id: str) -> dict:
    """Retrieves comprehensive hydration data for a specific user"""
    total_intake = get_today_total(user_id)
    goal = get_personalized_goal(user_id)
    patterns = analyze_user_patterns(user_id)
    
    return {
        "current_intake": total_intake,
        "daily_goal": goal,
        "progress_percentage": (total_intake/goal) * 100,
        "peak_hour": patterns["peak_hour"],
        "least_hydrated_day": patterns["worst_day"]
    }
```

### **Agent Configuration:**
- **Model**: Groq LLaMA3-70B (Ultra-fast inference - 500+ tokens/second)
- **Tools**: Custom hydration tracking and analysis functions
- **Memory**: Conversation context for personalized responses
- **Temperature**: Optimized for consistent, helpful coaching

---

## 📊 Analytics & Insights

| Feature | Description | Technical Implementation |
|---------|-------------|-------------------------|
| **Trend Visualization** | Weekly hydration charts | Pandas + Streamlit plotting |
| **Pattern Recognition** | Peak hours & day analysis | SQL aggregation + statistical analysis |
| **Goal Personalization** | AI-generated targets | Machine learning on user history |
| **Progress Tracking** | Real-time goal monitoring | Live database queries |
| **Habit Insights** | Behavioral pattern discovery | Time-series analysis |

---

## 🚀 Why This Project Stands Out

### **For Technical Evaluation:**

1. **Modern AI Stack**: Cutting-edge integration of LangChain agents with Groq LLMs
2. **Practical Application**: Solves real-world health tracking with measurable impact
3. **Clean Architecture**: Well-structured, modular codebase with clear separation of concerns
4. **Scalable Design**: Multi-user support demonstrates production-ready system thinking
5. **Full-Stack Mastery**: Seamless integration of frontend, backend, database, and AI

### **Technical Highlights:**

- ⚡ **Performance**: Groq provides 10x faster inference than traditional LLM APIs
- 🔧 **Flexibility**: Custom LangChain tools enable easy feature expansion
- 📈 **Scalability**: Database design supports thousands of concurrent users
- 🛠️ **Maintainability**: Modular architecture with clear API contracts
- 🧠 **Intelligence**: Agentic AI that learns and adapts to user behavior

---

## 🔑 Groq AI Integration

### **Why Groq?**
- **⚡ Speed**: 500+ tokens/second inference (10x faster than competitors)
- **💰 Cost-effective**: Competitive pricing for high-volume usage
- **🔒 Reliability**: 99.9% uptime with global infrastructure
- **🎯 Accuracy**: State-of-the-art LLaMA3 models with excellent reasoning

### **Setup Process:**
1. **Get API Key**: Visit [console.groq.com/keys](https://console.groq.com/keys)
2. **Add to Environment**: `export GROQ_API_KEY="your_key"`
3. **Configure in App**: Automatic detection and initialization

---

## 🧪 Testing & Development

### **API Testing**
Use the interactive API documentation at `/docs` to test all endpoints:
- Log water intake for multiple users
- Retrieve hydration analytics and trends
- Test AI agent responses

### **Generate Test Data**
```bash
# Simulate hydration logs for testing patterns
curl -X POST "localhost:8000/simulate-logs/testuser"
```

---

## 🎯 Future Roadmap

- [ ] **📧 Weekly Reports** - Automated email summaries with downloadable PDF insights
- [ ] **🏆 Gamification** - Hydration streaks, achievements, and social challenges
- [ ] **⏰ Smart Reminders** - AI-powered notification scheduling based on patterns
- [ ] **📱 Mobile App** - Native iOS/Android application with offline sync
- [ ] **🔗 Wearable Integration** - Apple Watch, Fitbit, and other device connectivity
- [ ] **🤝 Social Features** - Share progress and compete with friends/family

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yourusername/hydromind/issues).

1. **Fork the Project**
2. **Create Feature Branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit Changes** (`git commit -m 'Add AmazingFeature'`)
4. **Push to Branch** (`git push origin feature/AmazingFeature`)
5. **Open Pull Request**

---

## 👨‍💻 Author

**Built with 💙 by Rushik**


---

<div align="center">

**🌊 Stay hydrated, stay healthy! 💧**

*Built with modern AI technology for a healthier tomorrow*

</div>
