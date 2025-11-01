import logging

def output_node(state):
    ''' Consolidates the output states received from various nodes for display to the user'''
    tool = ", ".join(state.selected_tools or [])
    result = "\n".join([str(item) for item in (state.tool_outputs or []) if item is not None])
    
    if not tool:
        logging.warning(f"No matching tool found for the user query: {state.user_query}")

        return {**state.dict(), "final_output": state.final_output}
        
    final = (
        # f"🧠 Reasoning: {reasoning}\n"
        f"🧰 Tools Used: {tool}\n"
        f"📊 Result: {result}\n"
        # f"📚 Context: {context}\n"
        
    )
    logging.info(f"Final output summary — Tool: {tool}, Result: {result}")

    return {**state.dict(), "final_output": final}
