from background_task import background

@background(schedule=60)
def send_otp_to_user(phone_number, otp):
    print(f"Sending OTP to {phone_number}: {otp}")
