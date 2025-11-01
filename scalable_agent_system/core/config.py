import os
from dotenv import load_dotenv
from openai import OpenAI
import logging

load_dotenv()

# Initialize OpenAI client (via OpenRouter)
def get_llm():
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )
# --- System Search Tool Keywords ---
system_search_keywords = [
    "what tools",
    "available tools",
    "system capabilities",
    "what can you do",
    "your capabilities",
    "list tools",
    "status of my last request",
    "my last request",
]


def get_system_capabilities_summary():

    available_tools = ["PayPalTool", "EmailTool"]
    apis = "OpenRouter(OpenAI-compatible)"
    selected_model = "mistral-7b-instruct"
    features = ["Logging", "Persistent Memory"]
    additional_tools = ['RAG Pipeline Tool', 'System Search Tool']

    summary = (
        f"System/Agent Capabilities Summary: "
        f"Available tools = {', '.join(available_tools)} | "
        f"APIs = {apis} | "
        f"Model = {selected_model} | "
        f"Features = {', '.join(features)} | "
        f"Additional tools = {', '.join(additional_tools)} | "
    )
    return summary

#----------Configuration for Logging------------#
logging.basicConfig(
    filename='scalable_agent.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

def log_system_capabilities():
    logging.info(get_system_capabilities_summary())