import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate

from tools import (
    search_destinations,
    get_attractions,
    get_travel_tips,
    compare_destinations,
    list_all_categories
)

load_dotenv()

# ---------------- TOOLS ----------------
TOOLS = [
    search_destinations,
    get_attractions,
    get_travel_tips,
    compare_destinations,
    list_all_categories
]

# ---------------- PROMPT (FIXED tool_names issue) ----------------
prompt = PromptTemplate.from_template("""
You are Serendib AI 🇱🇰, a Sri Lankan travel assistant.

You help users explore:
- beaches
- wildlife safaris
- cultural sites
- nature hikes
- travel planning

You have access to tools.

TOOLS:
{tools}

Tool Names:
{tool_names}

IMPORTANT RULES:
- Always use tools when needed
- Keep answers simple and helpful
- Avoid long unnecessary text
- Focus on Sri Lanka tourism

Format:
Question: {input}
Thought: think step by step
Action: tool name
Action Input: input for tool
Observation: result
Final Answer: response to user

Begin!

Question: {input}
{agent_scratchpad}
""")

# ---------------- MEMORY ----------------
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# ---------------- AGENT CREATOR ----------------
def create_tourism_agent():

    # ✅ FIXED MODEL (NO DEPRECATED MODELS)
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.4
    )

    agent = create_react_agent(
        llm=llm,
        tools=TOOLS,
        prompt=prompt
    )

    executor = AgentExecutor(
        agent=agent,
        tools=TOOLS,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True
    )

    return executor