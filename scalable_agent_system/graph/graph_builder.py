from langgraph.graph import StateGraph
from graph.state_schema import AgentState
from graph.nodes.tool_router_node import tool_router_node
from graph.nodes.tool_layer_node import tool_layer_node
from graph.nodes.output_node import output_node

def build_graph():
     
    """Constructs and compiles the modular LangGraph agent workflow.

    This function defines the directed workflow graph for the intelligent agent 
    using LangGraph. Each node in the graph represents a functional stage in the 
    reasoning and execution pipeline (e.g., reasoning, tool routing, tool execution, 
    and output generation). The nodes are connected in a logical sequence that allows 
    the agent to reason about user queries, choose appropriate tools, execute tasks, 
    and return the final response.

    Workflow:
        reasoning → router → tool_layer → reasoning → output

    Returns:
        langgraph.graph.CompiledGraph: The compiled graph ready for invocation.

    """
    graph = StateGraph(AgentState)
    # Core nodes
    graph.add_node("router", tool_router_node)
    graph.add_node("tool_layer", tool_layer_node)
    graph.add_node("output", output_node)

    # Set entry and finish points
    graph.set_entry_point("router")
    graph.set_finish_point("output")

    # Connect the graph nodes
    graph.add_edge("router", "tool_layer")

    # Finally go to output
    graph.add_edge("tool_layer", "output")

    return graph.compile()

     

    