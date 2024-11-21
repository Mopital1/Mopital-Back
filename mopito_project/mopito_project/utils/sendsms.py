import requests
import random
import string


from config.settings.base import SMS_API_PASSWORD, SMS_API_URL, SMS_API_USER_ID

def send_otp(phone_number, otp, sender_name="Mopital"):
    
    message = f"Votre code de vérification est {otp}\n\n Your verification code is {otp}"
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


def codeGenerator(chars=string.ascii_uppercase + string.digits, N=5):
    """
    otp code generator
    """
    
    return ''.join(random.choice(chars) for _ in range(N))

def phoneNumberGenerator(chars=string.digits, N=8):
    """
    fake phone number generator
    """
    return '6'.join(random.choice(chars) for _ in range(N))
