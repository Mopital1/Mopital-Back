from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework import filters, mixins, status

from mopito_project.core.api.views import BaseModelViewSet
from mopito_project.actors.models import Patients, Staffs, Subscription, TimeSlot
from mopito_project.actors.api.serializers import PatientDetailSerializer, PatientSerializer, StaffDetailSerializer, StaffSerializer, SubscriptionDetailSerializer, SubscriptionSerializer, TimeSlotDetailSerializer, TimeSlotSerializer


class PatientViewSet(BaseModelViewSet, mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.CreateModelMixin,):
    queryset = Patients.objects.filter(is_active=True)
    serializer_class = PatientSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "user__profile_id": ['exact'],
        "user__profile__name": ['exact', 'contains'],
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
        "user__profile__name": ['exact', 'contains'],
        "user__profile__phone_number": ['exact', 'contains'],
        "staff_parent_id": ['exact'],
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
    queryset = TimeSlot.objects.filter(is_active=True)
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

class SubscriptionsViewSet(BaseModelViewSet, mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.CreateModelMixin,):
    queryset = Subscription.objects.filter(is_active=True)
    serializer_class = SubscriptionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "patient_id": ['exact'],
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