import requests

from config.settings.base import SMS_API_PASSWORD, SMS_API_URL, SMS_API_USER_ID

def send_otp(phone_number, otp, sender_name="Mopital"):
    
    message = f"Votre code de vérification est {otp}"
    url = SMS_API_URL

    payload = {
        "user_id": SMS_API_USER_ID,
        "message": message,
        "password": SMS_API_PASSWORD,
        "phone_str": phone_number,
        "sender_name": sender_name
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        # return response.json()
        print(response.json())
    else:
        # return response.raise_for_status()
        print(response.raise_for_status())