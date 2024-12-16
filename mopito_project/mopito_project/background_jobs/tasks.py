# from background_task import background
# from mopito_project.appointments.models import Appointment
# from datetime import datetime, timedelta



# def mark_missed_app():
#     print("Hello world")
#     appointments = Appointment.objects.filter(is_active=True)
#     current_date = datetime.now()
#     for appointment in appointments:
#         if appointment.status == 'PENDING' and appointment.appointment_date < current_date:
#             appointment.status = 'MISSED'
#             appointment.save()


# def notif_relance():
#     print("You have an appointment")
#     appointments = Appointment.objects.filter(is_active=True)
#     current_date = datetime.now()
#     tomorrow = current_date + timedelta(days=1)
#     for appointment in appointments:
#         if appointment.appointment_date == tomorrow:
#             # Assuming there's a method to send notifications to patients and staffs
#             # appointment.patient.send_notification("Your appointment is tomorrow.")
#             # appointment.staff.send_notification("You have an appointment tomorrow.")
#             print("You have an appointment tomorrow.")
    

# @background(schedule=10)
# def send_otp_to_user():
#     print("Sending OTP to 693205269: 1200QE")
#     notif_relance()
#     mark_missed_app()
    

#     # send_otp_to_user(repeat=BT.DAILY, verbose_name="send_otp_to_user")
 