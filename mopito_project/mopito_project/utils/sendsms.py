import requests
import random
import string
from django.template.loader import render_to_string

from config.settings.base import SMS_API_PASSWORD, SMS_API_URL, SMS_API_USER_ID

def send_otp(phone_number, otp, sender_name="Mopital"):
    
    message = f"Votre code de vérification est {otp}\n\n Your verification code is {otp}\n {SMS_API_USER_ID}"
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

def send_appoint_notification(appointment, template, phone_number, sender_name="Mopital"):
        # message = f"Vous avez un rendez-vous à venir\n\n You have an upcoming appointment"
        staff_profile = appointment.staff.user.profile
        appointment_date = appointment.appointment_date.strftime("%d-%m-%Y")
        appointment_time = appointment.appointment_date.strftime("%H:%M")
        patient_profile = appointment.patient.user.profile
        message = render_to_string(template, {'staff_profile': staff_profile,
                                            'appointment_date': appointment_date,
                                            'patient_profile': patient_profile,
                                            'appointment_time': appointment_time,
                                            'sender_id': SMS_API_USER_ID
                                            }
                                   )
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
