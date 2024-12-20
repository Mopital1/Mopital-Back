
from mopito_project.appointments.models import Appointment, Consultation, Notification, Review, Advertise
from mopito_project.core.api.serializers import BaseSerializer
from mopito_project.actors.api.serializers import PatientDetailSerializer, StaffDetailSerializer
from rest_framework import serializers
from django.db import transaction
from datetime import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404

from mopito_project.actors.models import Patients, Staffs
from mopito_project.utils.sendsms import phoneNumberGenerator, send_appoint_notification
from mopito_project.users.models import Profile, User

class AppointmentSerializer(BaseSerializer):
    patient = serializers.UUIDField(required=False)
    staff = serializers.UUIDField(required=False)
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
    
    def validate(self, validated_data):
        user = self.context['request'].user
        appointment_date = validated_data.get("appointment_date")

        # Validation de la date de rendez-vous
        if appointment_date and appointment_date.tzinfo is None:
            appointment_date = timezone.make_aware(appointment_date) 
        current_time = timezone.now()
        if appointment_date <= current_time:
            raise serializers.ValidationError("La date du rendez-vous doit être dans le futur.")

        # Validation du patient
        patient_uuid = validated_data.get("patient")
        if patient_uuid:
            validated_data["patient"] = get_object_or_404(Patients, id=patient_uuid)
            
        else:
            validated_data["patient"] = user.patient

        # Validation du personnel
        staff_uuid = validated_data.get("staff")
        if staff_uuid:
            validated_data["staff"] = get_object_or_404(Staffs, id=staff_uuid)
            
        return validated_data

    def create(self, validated_data):
        """
        créer un rendez vous pour un patient ou pour son proche
        """
        user = self.context['request'].user

        try:
            appointment = Appointment.objects.create(**validated_data)
            # envoyer une notification au patient
            if appointment.patient.patient_parent:
                # parent_appoint_confirmation.txt
                send_appoint_notification(appointment, 'sms/parent_appoint_confirmation.txt', user.profile.phone_number)
            else:
                send_appoint_notification(appointment, 'sms/patient_appoint_confirmation.txt', user.profile.phone_number)
            return appointment
        except Exception as e:
            raise serializers.ValidationError(f"Erreur lors de la création du rendez-vous : {e}")

class UpdateAppointmentSerializer(BaseSerializer):
    patient = serializers.UUIDField(required=False)
    staff = serializers.UUIDField(required=False)
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

    def update(self, instance, validated_data):
            current_date = timezone.now()
            
            if instance.patient_update_count <= 3:  
                instance.appointment_date = validated_data.get("appointment_date", instance.appointment_date)  
                instance.description = validated_data.get("description", instance.description)
                instance.patient = validated_data.get("patient", instance.patient)
                instance.staff = validated_data.get("staff", instance.staff)
                instance.status = validated_data.get("status", instance.status)
            else:
                raise serializers.ValidationError("La date du rendez-vous a été modifiée plus de 3 fois.")
            
            if "appointment_date" in validated_data:
                    appointment_date = validated_data.get("appointment_date")
                    # Validation de la date de rendez-vous
                    if appointment_date and appointment_date.tzinfo is None:
                        appointment_date = timezone.make_aware(appointment_date) 
                    if appointment_date >= current_date:
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

class AdvertiseSerializer(BaseSerializer):
    class Meta:
        model = Advertise
        fields = (
            "id",
            "title",
            "advertise_image",
            "content",
            "redirect_link",
            "redirect_link_text",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at",)
