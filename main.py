# main.py

from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from . import tools  # ✅ import the tool functions from tools.py
import os
from dotenv import load_dotenv

# ✅ Load environment variables (like OPENAI_API_KEY)
load_dotenv()

# === LLM Configuration ===
llm = ChatOpenAI(temperature=0, model="gpt-4")

# === Define Tool Wrappers ===
all_tools = [
    Tool.from_function(func=tools.list_cities),
    Tool.from_function(func=tools.query_zip_scores),
    Tool.from_function(func=tools.get_geojson_for_city),
    Tool.from_function(func=tools.get_zip_details),
]

# === Initialize Agent ===
agent = initialize_agent(
    tools=all_tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
)

# === Interactive CLI (for now) ===
if __name__ == "__main__":
    print("🧠 Circle30 EV Underserved Area Agent")
    print("💬 Ask about underserved ZIPs, city EV access, etc.\n")

    while True:
        query = input("🔎 Query: ")
        if query.lower() in ["exit", "quit"]:
            break
        response = agent.run(query)
        print(f"\n📊 Answer:\n{response}\n")
