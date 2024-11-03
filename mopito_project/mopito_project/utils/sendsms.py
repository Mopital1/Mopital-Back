import requests

def send_otp(user_id, message, password, phone_str, sender_name="Mopito"):
    url = "https://mboadeals.net/api/v1/sms/sendsms"
    payload = {
        "user_id": user_id,
        "message": message,
        "password": password,
        "phone_str": phone_str,
        "sender_name": sender_name
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()