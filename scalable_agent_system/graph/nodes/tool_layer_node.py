from tools.paypal_tool import list_invoices, get_invoice, create_invoice
from tools.email_tool import send_email
import re
import logging
from tools.system_search_tool import system_query_handler
from tools.rag_tool import rag_query_handler

def tool_layer_node(state):
    """Execute the tool corresponding to the selected routing decision.

    Based on the selected_tool in the state, invokes the relevant function 
    such as PayPalTool (for invoice retrieval) or EmailTool (for sending emails).

    Args:
        state: AgentState object containing user query and selected tool.

    Returns:
        dict: Updated state containing the tool's output.
    """

    tools = state.selected_tools or []
    query = state.user_query
    outputs = []

    invoice_data = None  # keep to pass between tools

    for tool in tools:
        

        if tool == "paypaltool":
            match = re.search(r"INV-\d+", query)
            if match:
                invoice_id = match.group(0)
                invoice_data = get_invoice(invoice_id)
                outputs.append(get_invoice(invoice_id))
            else:
                outputs.append("No valid invoice ID found. Provide a valid invoice ID")
                break
         
        elif tool == "emailtool":
            subject = " "
            content = "Your invoice is attached."

            # if we already got invoice data, include it in email
            if invoice_data:
                # subject = f"Invoice {json.loads(invoice_data)['invoice_id']}"
                subject = f"Invoice ID: {invoice_id}"
                content = f"Here is your invoice:\n{invoice_data}"

            result = send_email("customer@example.com", subject,content)
            outputs.append(result)

        elif tool == "ragtool":
            logging.info(f"RAGTool triggered by user query:{query}")
            outputs.append(rag_query_handler(query))
            
        elif tool == "systemsearchtool":
            logging.info(f"SystemSearchTool triggered by user query:{query}")
            try:
                outputs.append(system_query_handler(query))
                                
            except Exception as e:
                logging.error(f"Error while handling system search query: {str(e)}")
                outputs.append("Sorry, something went wrong while searching system capabilities.")
                
    return {**state.dict(), "tool_outputs": outputs}
