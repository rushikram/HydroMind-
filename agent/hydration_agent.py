from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_groq import ChatGroq
from agent.tools import get_tools

def run_agent(user_input: str, api_key: str, goal_ml: int, user_id: str) -> str:
    """
    Executes a hydration assistant agent using LangChain + Groq LLaMA model.

    Parameters:
    - user_input: The question asked by the user.
    - api_key: Groq API key for LLaMA model access.
    - goal_ml: User's daily hydration goal to personalize response.
    - user_id: Unique user identifier for hydration data retrieval.

    Returns:
    - A string response from the agent.
    """
    try:
        # Initialize the LLM using Groq's LLaMA 3 model
        llm = ChatGroq(api_key=api_key, model_name="llama3-70b-8192")

        # Load hydration-related tools (today’s intake, trend, goal, insights)
        tools = get_tools(goal_ml, user_id)

        # Initialize the LangChain agent with toolset
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True  # Set to False if you want to hide internal steps
        )

        # Enrich prompt with hydration goal context
        enriched_prompt = f"{user_input.strip()} (Hydration goal: {goal_ml} ml)"
        return agent.run(enriched_prompt)

    except Exception as e:
        return f"[Agent Error] {str(e)}"
