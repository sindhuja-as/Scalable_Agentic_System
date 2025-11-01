from langchain_core.tools import Tool
import json

def send_email(to, subject, content) -> str:
    """
    payload is a JSON string: {"to":"x@x", "subject":"...", "body":"..."}
    In prototype we only simulate send and return success.
    """
    try:
        # obj = json.loads(payload)
        # to = obj.get("to")
        # subject = obj.get("subject", "")
        # here you'd hook to an SMTP or email API in production
        return f"Email simulated: sent to {to}"
    except Exception as e:
        return f"send_email error: {e}"

email_tool = Tool(
    name="Email_Send",
    func=send_email,
    description='Send an email. Input should be JSON string with "to", "subject", and "body".'
)
