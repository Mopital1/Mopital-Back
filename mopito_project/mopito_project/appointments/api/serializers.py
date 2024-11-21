
from mopito_project.appointments.models import Appointment, Consultation, Notification, Review
from mopito_project.core.api.serializers import BaseSerializer
from mopito_project.actors.api.serializers import PatientDetailSerializer, StaffDetailSerializer
from rest_framework import serializers
from django.db import transaction


from mopito_project.actors.models import Patients
from mopito_project.utils.sendsms import phoneNumberGenerator
from mopito_project.users.models import Profile, User

class AppointmentSerializer(BaseSerializer):
    child_first_name = serializers.CharField()
    child_last_name = serializers.CharField()
    class Meta:
        model = Appointment
        fields = (
            "id",
            "appointment_date",
            "description",
            "patient",
            "staff",
            "child_first_name",
            "child_last_name",
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
        child_first_name = validated_data.pop("child_first_name", None)
        child_last_name = validated_data.pop("child_last_name", None)
        try:
            with transaction.atomic():
                if validated_data.get("patient") is None:
                    # creer le patient fils du patient courant
                    phone_number = phoneNumberGenerator()
                    profile = Profile.objects.create(first_name=child_first_name, 
                                                    last_name=child_last_name,
                                                    phone_number=phone_number
                                                    )
                    patient = Patients.objects.create(patient_parent=user.patient)
                    email = f"{profile.phone_number}@mopital.com"
                    user = User.objects.create(profile_id=profile.id,
                                            patient_id=patient.id,
                                            user_typ="PATIENT",
                                            email=email)
                    validated_data["patient"] = patient
                
                appointment = Appointment.objects.create(**validated_data)
                return appointment
        except Exception as e:
            raise serializers.ValidationError(f"Erreur lors de la création du rendez-vous : {e}")
            


        #appointment = Appointment.objects.create(**validated_data)



class AppointmentDetailSerializer(BaseSerializer):
    staff = StaffDetailSerializer()
    patient = PatientDetailSerializer()
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