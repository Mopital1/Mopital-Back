from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework import filters, mixins, status

from mopito_project.core.api.views import BaseModelViewSet
from mopito_project.actors.models import Clinics,  Patients, Staffs, Subscriptions, TimeSlots
from actors.api.serializers import ClinicDetailSerializer, ClinicSerializer, PatientDetailSerializer, PatientSerializer, StaffDetailSerializer, StaffSerializer, SubscriptionDetailSerializer, SubscriptionSerializer, TimeSlotDetailSerializer, TimeSlotSerializer
from mopito_project.users.api.serializers import CompleteProfileSerializer, CreateProfileSerializer, ProfileSerializer
from mopito_project.users.models import Profile, User


class PatientViewSet(BaseModelViewSet, mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.CreateModelMixin,):
    queryset = Patients.objects.filter(is_active=True)
    serializer_class = PatientSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
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
        return PatientSerializer

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