# tools/paypal_tool.py
import json
import os
from langchain_core.tools import Tool

DATA_PATH = "data/paypal_mock_data.json"
os.makedirs("data", exist_ok=True)
def _load():
    """
    Load and return data from the JSON file defined by DATA_PATH.

    This function reads the contents of the JSON file located at DATA_PATH
    using UTF-8 encoding and returns the parsed data as a Python object.
    It is primarily used as a helper function to access stored invoice or
    configuration data for other tool operations.

    Returns:
        dict: The parsed contents of the JSON file.
    """
    with open(DATA_PATH, "r", encoding="utf8") as f:
        return json.load(f)

def get_invoice(invoice_id: str) -> str:
    """
    Return invoice details for a given invoice_id.
    Input: invoice id string
    """
    data = _load()
    for inv in data.get("invoices", []):
        if inv["invoice_id"].lower() == invoice_id.lower():
            return json.dumps(inv)
    return f"Invoice {invoice_id} not found."

def list_invoices() -> str:
    """
    Retrieve and return all available invoices as a JSON string.

    This function loads the stored invoice data using the `_load()` helper function,
    extracts the list of invoices from the dataset, and serializes it into a JSON-formatted string.
    If no invoices are found, it returns an empty list in JSON format.

    Returns:
        str: A JSON-formatted string containing all invoice records.
    """
    data = _load()
    return json.dumps(data.get("invoices", []))

def create_invoice(payload: str) -> str:
    """
    payload: JSON string with keys amount, customer
    For prototype we just append to file
    """
    try:
        obj = json.loads(payload)
        data = _load()
        next_id = f"INV-{1000 + len(data.get('invoices', [])) + 1}"
        inv = {
            "invoice_id": next_id,
            "amount": float(obj.get("amount", 0)),
            "currency": obj.get("currency", "USD"),
            "customer": obj.get("customer"),
            "status": "SENT"
        }
        data.setdefault("invoices", []).append(inv)
        with open(DATA_PATH, "w", encoding="utf8") as f:
            json.dump(data, f, indent=2)
        return json.dumps(inv)
    except Exception as e:
        return f"create_invoice error: {e}"

paypal_get_invoice = Tool(
    name="PayPal_GetInvoice",
    func=get_invoice,
    description="Get a PayPal invoice by ID. Input is invoice id string."
)

paypal_list_invoices = Tool(
    name="PayPal_ListInvoices",
    func=lambda q: list_invoices(),
    description="List PayPal invoices."
)

paypal_create_invoice = Tool(
    name="PayPal_CreateInvoice",
    func=create_invoice,
    description='Create a new invoice. Input is JSON string with amount and customer fields e.g. {"amount":50,"customer":"a@b.com"}'
)
