"""
Placeholder for SMS gateway integration services.
"""

def send_sms(phone_number: str, message: str):
    """
    Simulates sending an SMS message via the sms.ir gateway.
    In a real application, this would contain the API call logic.
    """
    print("--- SIMULATING SMS ---")
    print(f"To: {phone_number}")
    print(f"Message: {message}")
    print("----------------------")
    # In a real implementation, you would return a success boolean and a transaction ID
    return True
