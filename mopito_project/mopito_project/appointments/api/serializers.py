
from mopito_project.appointments.models import Appointment, Consultation, Notification, Review
from mopito_project.core.api.serializers import BaseSerializer
from mopito_project.actors.api.serializers import PatientDetailSerializer, StaffDetailSerializer
from rest_framework import serializers
from django.db import transaction
from datetime import datetime


from mopito_project.actors.models import Patients
from mopito_project.utils.sendsms import phoneNumberGenerator, send_appoint_notification
from mopito_project.users.models import Profile, User

class AppointmentSerializer(BaseSerializer):
    
    class Meta:
        model = Appointment
        fields = (
            "id",
            "appointment_date",
            "description",
            "patient",
            "staff",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at",)

    def create(self, validated_data):
        """
        créer un rendez vous pour un patient ou pour son proche
        """
        user = self.context['request'].user
        try:
            appointment_date = validated_data.get("appointment_date")
            if appointment_date <= datetime.now():
                raise serializers.ValidationError("La date du rendez-vous doit être dans le futur.")
            appointment = Appointment.objects.create(**validated_data)
            # envoyer une notification au staff
            # staff_phone_number = appointment.staff.user.profile.phone_number
            # send_appoint_notification(appointment,'sms/staff_appoint_notification.txt', staff_phone_number)
            # envoyer une notification au patient
            send_appoint_notification(appointment,'sms/patient_appoint_confirmation.txt', user.profile.phone_number)
            return appointment
        except Exception as e:
            raise serializers.ValidationError(f"Erreur lors de la création du rendez-vous : {e}")
            
    def update(self, instance, validated_data):
            current_date = datetime.now()
            
            if instance.patient_update_count <= 3:  
                instance.appointment_date = validated_data.get("appointment_date", instance.appointment_date)  
                instance.description = validated_data.get("description", instance.description)
                instance.patient = validated_data.get("patient", instance.patient)
                instance.staff = validated_data.get("staff", instance.staff)
                instance.status = validated_data.get("status", instance.status)
            else:
                raise serializers.ValidationError("La date du rendez-vous a été modifiée plus de 3 fois.")
            
            if "appointment_date" in validated_data:
                    if validated_data.get("appointment_date") > current_date:
                        instance.patient_update_count += 1
                    else:
                        raise serializers.ValidationError("La date du rendez-vous doit être dans le futur.")
                
            # Gestion des exceptions lors de la sauvegarde
            try:
                instance.save()
            except Exception as e:
                raise serializers.ValidationError(f"Erreur lors de la mise à jour du rendez-vous : {e}")
            
            return instance
            #appointment = Appointment.objects.create(**validated_data)



class AppointmentDetailSerializer(BaseSerializer):
    staff = StaffDetailSerializer()
    patient = PatientDetailSerializer()
    class Meta:
        model = Appointment
        fields = (
            "id",
            "appointment_date",
            "patient_update_count",
            "description",
            "patient",
            "staff",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at",)

    


class ReviewSerializer(BaseSerializer):
    class Meta:
        model = Review
        fields = (
            "id",
            "rating",
            "comment",
            "appointment",
            "review_date",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at",)

class ReviewDetailSerializer(BaseSerializer):
    appointment = AppointmentDetailSerializer()
    class Meta:
        model = Review
        fields = (
            "id",
            "rating",
            "comment",
            "appointment",
            "review_date",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at",)

class NotificationSerializer(BaseSerializer):
    class Meta:
        model = Notification
        fields = (
            "id",
            "notification_date",
            "content",
            "notification_type",
            "appointment",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at",)

class NotificationDetailSerializer(BaseSerializer):
    appointment = AppointmentDetailSerializer()
    class Meta:
        model = Notification
        fields = (
            "id",
            "notification_date",
            "content",
            "notification_type",
            "appointment",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at",)

class ConsultationSerializer(BaseSerializer):
    class Meta:
        model = Consultation
        fields = (
            "id",
            "consultation_date",
            "prescription",
            "result",
            "antecedent",
            "appointment",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at",)

class ConsultationDetailSerializer(BaseSerializer):
    appointment = AppointmentDetailSerializer()
    class Meta:
        model = Consultation
        fields = (
            "id",
            "consultation_date",
            "prescription",
            "result",
            "antecedent",
            "appointment",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at",)