from core.config import get_llm
import re

def tool_router_node(state):
    """Routes the user query to the appropriate tool or tool chain based on intent.
    This function analyzes the user's query using an LLM to determine which tool(s) should handle the request. 
    It constructs a routing prompt that lists all available tools and rules for their usage. Based on the LLM's 
    response, it identifies one or more tools (e.g., PayPalTool, EmailTool) to execute in sequence. If no 
    relevant tool is found, it triggers a fallback response.

    Args:
        state (AgentState): The current agent state containing the user query 
            and any previous reasoning or context.

    Returns:
        dict: Updated state with the following key(s):
            - tools_used (list[str]): The list of tools selected by the router.
            - selected_tool (str): The first tool to execute next.
            - fallback_message (Optional[str]): Default message for irrelevant queries.
    """
    llm = get_llm()
    query = state.user_query

    router_prompt = f"""
    You are an intelligent reasoning and tool routing assistant for a modular AI agent.
    Your job is to **analyze the user's intent** and decide which tool(s) should be used — in the correct order.

    You CANNOT answer general-purpose questions or casual conversation.
    If the query is irrelevant or unrelated to invoices or emails, reply exactly with:
    "Sorry I am unable to understand. Please ask a valid question."
    You have access to the following tools:

    1. PayPalTool — retrieves invoice details and manages transactions.
    2. EmailTool — sends emails to recipients.
    3. SystemSearchTool- Provides Agent and system related information.
    4. RAGTool- Provides information about Blaupunkt Stereo from "C:\\Users\\Arun\\Documents\\scalable_agent_system\\graph\\nodes\\Blaupunkt_Manual.pdf" alone
   
    Rules for routing:

    -IF the query involves : 'What tools are available?' or'What tools manage invoices?' or'What's the system status?' or 'what is the status of my previous request?'
        or 'what is the capability of the system?'use SystemSearchTool.
    - If the query involves "email invoice", "send invoice", or "attach invoice",
      use BOTH PayPalTool (to fetch invoice details) and EmailTool (to send it), ALWAYS return tools in their order order of dependency: PayPalTool, EmailTool.
      this is because only after accessing invoice from PayPal too, email could be sent.
    - If the query mentions only "get invoice" or "show invoice", use PayPalTool only.
    - If the query is just system and status related use SystemSearchTool only
    - If the query is about Blaupunkt car stereo product features use RAGTool only    
    - Always return tools in the correct sequence for dependency (e.g. PayPalTool -> EmailTool).

    User Query: {query}
    
    Respond ONLY with a comma-separated list of tool names in order of use.
    Example: PayPalTool, EmailTool
    """

    response = llm.chat.completions.create(
        model="mistralai/mistral-7b-instruct-v0.2",
        messages=[{"role": "user", "content": router_prompt}]
    )

    raw_output = response.choices[0].message.content.strip()
    state.selected_tools = []

    # Extract tool names as a list safely
    tools = re.findall(r"PayPalTool|EmailTool|SystemSearchTool|RAGTool", raw_output, flags=re.IGNORECASE)
  
    if not tools:
        fallback_message = (
            "I couldn’t find a suitable tool to handle your request. "
            "Please try rephrasing or ask something related to invoices, email, system capabilities or Product details of Blaupunkt Stereo ."
        )

        # Directly jump to output
        return {
            **state.dict(),
            "selected_tool": None,
            "tools_used": [],
            "tool_output": fallback_message,
            "final_output": fallback_message,
        }

    # Normalize capitalization
    tools = [t.lower() for t in tools]
    return {**state.dict(), "selected_tools": tools}
