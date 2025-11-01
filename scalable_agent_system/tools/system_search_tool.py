import re
from core.config import get_system_capabilities_summary
import logging
from pathlib import Path

LOG_FILE = Path("scalable_agent.log")
def system_query_handler(query):
    query_lower = query.lower()
    if "last request" in query_lower or "previous request" in query_lower or "status" in query_lower:
        logging.info("System Search Tool: User requested status of last request.")
        return get_last_request_status()
    elif "system" in query_lower or "agent" in query_lower or "capability" in query_lower or "available" in query_lower or "tools" in query_lower or "show tools" in query_lower:
        return(get_system_capabilities_summary())
    else:
        logging.info("System Search Tool: Query not matched to known patterns.")
        return "I can help with: checking system capabilities or last request status."
    
def get_last_request_status() -> str:
    """
    Reads the last relevant log entry from scalable_agent.log
    and returns a human-friendly summary.
    """
    if not LOG_FILE.exists():
        return "No log file found. It seems the system has not processed any requests yet."

    try:
        with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()


        for line in reversed(lines):
            if "Final output summary" in line:
                return format_last_request_entry(line)

        return "No recent request summary found in logs."

    except Exception as e:
        logging.error(f"Error reading log file: {e}")
        return f"Unable to retrieve last request status. ({e})"


def format_last_request_entry(line: str) -> str:
    """
    Converts a 'Final output summary' log entry into a readable format.
    """
    try:
        # Example: "2025-11-01 00:29:45,689 - INFO - Final output summary – Tool: systemsearchtool, Result: ..."
        timestamp, level, message = line.strip().split(" - ", 2)
        message = message.replace("Final output summary", "").strip(" –:")  # clean formatting
        return f"Last Request ({timestamp}): {message}"
    except ValueError:

        return f"Last Request Log: {line.strip()}"
