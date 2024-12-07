from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework import filters, mixins, status
from django.db import transaction

from mopito_project.core.api.views import BaseModelViewSet
from mopito_project.actors.models import Clinics,  Patients, Staffs, Subscriptions, TimeSlots
from actors.api.serializers import ClinicDetailSerializer, ClinicSerializer, NearPatientSerializer, PatientDetailSerializer, PatientSerializer, StaffDetailSerializer, StaffSerializer, SubscriptionDetailSerializer, SubscriptionSerializer, TimeSlotDetailSerializer, TimeSlotSerializer, UpdatePatientSerializer

from mopito_project.utils.sendsms import phoneNumberGenerator
from mopito_project.users.api.serializers import CompleteProfileSerializer, CreateProfileSerializer, ProfileSerializer
from mopito_project.users.models import Profile, User


class PatientViewSet(BaseModelViewSet, mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.CreateModelMixin,):
    queryset = Patients.objects.filter(is_active=True)
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "user__id": ['exact'],
        "user__profile_id": ['exact'],
        "user__profile__first_name": ['exact', 'contains'],
        "user__profile__phone_number": ['exact', 'contains'],
        "patient_parent_id": ['exact'],
        "updated_at": ['gte', 'lte', 'exact', 'gt', 'lt'],
        "created_at": ['gte', 'lte', 'exact', 'gt', 'lt']
    }

    search_fields = ["user__profile__name", "user__profile__phone_number"]
    ordering_fields = ["updated_at", "created_at"]
    ordering = ["-updated_at", "-created_at"]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return PatientDetailSerializer
        if self.action == "update" or self.action == "partial_update":
            return UpdatePatientSerializer
        if self.action == "add_near_patient":
            return NearPatientSerializer
        return PatientSerializer
    
    @action(detail=False, methods=["post"])
    def add_near_patient(self, request, *args, **kwargs):
        serializer = NearPatientSerializer(data=request.data)
        user = self.request.user
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        email = serializer.validated_data.get("email")
        gender = serializer.validated_data.get("gender")
        height = serializer.validated_data.get("height")
        weight = serializer.validated_data.get("weight")
        phone_number = phoneNumberGenerator()
        if email is None:
            email = f"{phone_number}@mopito.com"
        username = email.split("@")[0]
        print("user", user)
        print("user patient", user.patient)
        if user.patient is None:
            return Response({"error": "You are not a patient"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                profile = Profile.objects.create(
                    username=username,
                    phone_number=phone_number,
                    gender=gender
                )
                new_user = User.objects.create(
                    profile_id=profile.id,
                    email=email,
                    user_typ="PATIENT"
                )
                patient = Patients.objects.create(
                    patient_parent_id=user.patient.id,
                    height=height,
                    weight=weight,
                )
                return Response({
                    "profile": profile.id,
                    "patient": patient.id
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class StaffViewSet(BaseModelViewSet, mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.CreateModelMixin,):
    queryset = Staffs.objects.filter(is_active=True)
    serializer_class = StaffSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "user__profile_id": ['exact'],
        "user__profile__first_name": ['exact', 'contains'],
        "user__profile__phone_number": ['exact', 'contains'],
        "type": ['exact'],
        "clinics__id": ['exact'],
        # "staff_parent_id": ['exact'],
        "updated_at": ['gte', 'lte', 'exact', 'gt', 'lt'],
        "created_at": ['gte', 'lte', 'exact', 'gt', 'lt']
    }

    search_fields = ["user__profile__name", "user__profile__phone_number"]
    ordering_fields = ["updated_at", "created_at"]
    ordering = ["-updated_at", "-created_at"]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return StaffDetailSerializer
        return StaffSerializer

class TimeSlotViewSet(BaseModelViewSet, mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.CreateModelMixin,):
    queryset = TimeSlots.objects.filter(is_active=True)
    serializer_class = TimeSlotSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "staff_id": ['exact'],
        "staff__user__profile__first_name": ['exact', 'contains'],
        "is_available": ['exact'],
        "start_time": ['gte', 'lte', 'exact', 'gt', 'lt'],
        "end_time": ['gte', 'lte', 'exact', 'gt', 'lt'],
        # "updated_at": ['gte', 'lte', 'exact', 'gt', 'lt'],
        # "created_at": ['gte', 'lte', 'exact', 'gt', 'lt']
    }
    search_fields = ["staff__user__profile__first_name"]
    ordering_fields = ["updated_at", "created_at"]
    ordering = ["-updated_at", "-created_at"]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return TimeSlotDetailSerializer
        return TimeSlotSerializer

class SubscriptionViewSet(BaseModelViewSet, mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.CreateModelMixin,):
    queryset = Subscriptions.objects.filter(is_active=True)
    serializer_class = SubscriptionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        # "patient_id": ['exact'],
        "staff_id": ['exact'],
        "start_date": ['gte', 'lte', 'exact', 'gt', 'lt'],
        "end_date": ['gte', 'lte', 'exact', 'gt', 'lt'],
        "updated_at": ['gte', 'lte', 'exact', 'gt', 'lt'],
        "created_at": ['gte', 'lte', 'exact', 'gt', 'lt']
    }
    search_fields = ["patient__user__profile__first_name", "staff__user__profile__first_name"]
    ordering_fields = ["updated_at", "created_at"]
    ordering = ["-updated_at", "-created_at"]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return SubscriptionDetailSerializer
        return SubscriptionSerializer

class ClinicViewSet(BaseModelViewSet, mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.CreateModelMixin,):
    queryset = Clinics.objects.filter(is_active=True)
    serializer_class = ClinicSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "name": ['exact', 'contains'],
        "address": ['exact', 'contains'],
        "phone_number": ['exact', 'contains'],
        "staffs__id": ['exact'],
        # "staffs__user__profile__first_name": ['exact', 'contains'],
        # "email": ['exact', 'contains'],
        "start_time": ['gte', 'lte', 'exact', 'gt', 'lt'],
        "end_time": ['gte', 'lte', 'exact', 'gt', 'lt'],
        "updated_at": ['gte', 'lte', 'exact', 'gt', 'lt'],
        "created_at": ['gte', 'lte', 'exact', 'gt', 'lt']
    }
    search_fields = ["name", "address", "phone_number", "email"]
    ordering_fields = ["updated_at", "created_at", "name"]
    ordering = ["-updated_at", "-created_at"]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return ClinicDetailSerializer
        return ClinicSerializer

class ProfileViewSet(
        BaseModelViewSet, 
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.CreateModelMixin,):
    queryset = Profile.objects.filter(is_active=True)
    serializer_class = ProfileSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["first_name", "last_name", "phone_number", "is_active"]
    search_fields = ["first_name", "last_name", "phone_number"]
    ordering_fields = ["updated_at", "created_at"]
    ordering = ["-updated_at", "-created_at"]
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateProfileSerializer
        if self.action == "complete_profile":
            return CompleteProfileSerializer
        return ProfileSerializer

    @action(detail=False, methods=["post"])
    # @permission_classes([AllowAny])
    def complete_profile(self, request, *args, **kwargs):
        serializer = CompleteProfileSerializer(data=request.data)
        user = self.request.user
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        
        # phone_number = serializer.validated_data.get("phone_number")
        height = serializer.validated_data.get("height")
        weight = serializer.validated_data.get("weight")

        patient = Patients.objects.create(height=height, weight=weight)
        # user = User.objects.get(profile__phone_number=phone_number)
        profile = user.profile
        
        profile.gender = serializer.validated_data.get("gender")
        profile.dob = serializer.validated_data.get("dob")
        profile.save()

        user = User.objects.get(profile=profile)
        user.email = serializer.validated_data.get("email")
        user.patient = patient
        user.save()

        return Response(serializer.data)


"""

class PatientReferentViewSet(BaseModelViewSet, mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.CreateModelMixin, ):
    
    queryset = PatientReferent.objects.filter(is_active=True)
    serializer_class = PatientReferentSerializers
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "phone_number": ['exact', 'contains'],
        "name": ['exact', 'contains'],
        "relation": ['exact', 'contains'],
        "updated_at": ['gte', 'lte', 'exact', 'gt', 'lt'],
        "created_at": ['gte', 'lte', 'exact', 'gt', 'lt']
    }
    search_fields = ["phone_number", "name"]
    ordering_fields = ["updated_at", "created_at", "name"]
    order = ["-updated_at", "-created_at", "name"]
    ordering = ["-updated_at", "-created_at", "name"]
    parser_classes = [FormParser, MultiPartParser, JSONParser]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return PatientReferentDetailSerializers
        return PatientReferentSerializers
"""