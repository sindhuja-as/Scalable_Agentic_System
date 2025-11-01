from graph.graph_builder import build_graph
from graph.state_schema import AgentState
from core.config import log_system_capabilities

def main():
    """
Main entry point for the Scalable LangGraph Agent System.

This module serves as the console-based interface for interacting with the
LangGraph-powered modular agent. It initializes the agent workflow graph,
accepts user input in real time, and routes queries through the defined
agent state pipeline to produce structured outputs.

Workflow:
    1. Logs system capabilities at startup.
    2. Builds the modular graph using `build_graph()`.
    3. Continuously accepts user queries until 'exit' or 'quit' is entered.
    4. Invokes the graph with the current `AgentState` and displays
       the agent's final output in a formatted manner.

Dependencies:
    - build_graph(): Constructs the complete LangGraph workflow.
    - AgentState: Defines the schema for query, selected tools, and outputs.
    - log_system_capabilities(): Logs system/agent configuration and available tools.

Usage:
    Run this file directly to start the interactive agent session:
        $ python main_langgraph.py
"""
    log_system_capabilities()
    print("🤖 Scalable LangGraph Agent System\n(Type 'exit' to quit)\n")

    graph = build_graph()

    while True:
        q = input("User: ")
        if q.lower() in ["exit", "quit"]:
            break

        state = AgentState(user_query=q)
        final_state = graph.invoke(state)

        print("\n=== Final Output ===")
        print(final_state["final_output"])
        print("====================\n")

if __name__ == "__main__":
    main()
