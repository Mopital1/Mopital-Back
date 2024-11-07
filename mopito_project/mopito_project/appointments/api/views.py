from django.shortcuts import render

from mopito_project.appointments.models import Appointment, Consultation, Notification, Review
from rest_framework import filters, mixins, status

from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend

from mopito_project.core.api.views import BaseModelViewSet
from mopito_project.appointments.api.serializers import AppointmentDetailSerializer, AppointmentSerializer, ConsultationSerializer, NotificationDetailSerializer, NotificationSerializer

# Create your views here.

class AppointmentViewSet(BaseModelViewSet, mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.CreateModelMixin, ):
    
    queryset = Appointment.objects.filter(is_active=True)
    serializer_class = AppointmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "patient_id": ['exact'],
        "staff_id": ['exact'],
        # "time_slot": ['exact'],
        "status": ['exact', 'contains'],
        "staff__user__profile__first_name": ['exact', 'contains'],
        "patient__user__profile__first_name": ['exact', 'contains'],
        "appointment_date": ['gte', 'lte', 'exact', 'gt', 'lt'],
        "updated_at": ['gte', 'lte', 'exact', 'gt', 'lt'],
        "created_at": ['gte', 'lte', 'exact', 'gt', 'lt'],
    
    }
    search_fields = ["patient__user__profile__first_name", "staff__user__profile__first_name"]
    ordering_fields = ["updated_at", "created_at", "patient"]
    order = ["-updated_at", "-created_at", "patient"]
    ordering = ["-updated_at", "-created_at", "patient"]
    parser_classes = [FormParser, MultiPartParser, JSONParser]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return AppointmentDetailSerializer
        return AppointmentSerializer
    
class ReviewViewSet(BaseModelViewSet, mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.CreateModelMixin, ):
    
    queryset = Review.objects.filter(is_active=True)
    serializer_class = AppointmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "appointment__patient_id": ['exact'],
        "appointment__staff_id": ['exact'],
        "appointment_id": ['exact'],
        "updated_at": ['gte', 'lte', 'exact', 'gt', 'lt'],
        "created_at": ['gte', 'lte', 'exact', 'gt', 'lt'],
        "review_date": ['gte', 'lte', 'exact', 'gt', 'lt']
    }
    # search_fields = ["patient", "staff"]
    ordering_fields = ["updated_at", "created_at", "patient"]
    order = ["-updated_at", "-created_at"]
    ordering = ["-updated_at", "-created_at"]
    parser_classes = [FormParser, MultiPartParser, JSONParser]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return AppointmentDetailSerializer
        return AppointmentSerializer
    
class ConsultationViewSet(BaseModelViewSet, mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.CreateModelMixin,):
    queryset = Consultation.objects.filter(is_active=True)
    serializer_class = ConsultationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "appointment__patient_id": ['exact'],
        "appointment__staff_id": ['exact'],
        "appointment_id": ['exact'],
        "updated_at": ['gte', 'lte', 'exact', 'gt', 'lt'],
        "created_at": ['gte', 'lte', 'exact', 'gt', 'lt'],
        "consultation_date": ['gte', 'lte', 'exact', 'gt', 'lt']
    }

class NotificationViewSet(BaseModelViewSet, mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.CreateModelMixin,):
    queryset = Notification.objects.filter(is_active=True)
    serializer_class = NotificationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "notification_type": ['exact'],
        "appointment__patient_id": ['exact'],
        "notification_date": ['gte', 'lte', 'exact', 'gt', 'lt'],
        "created_at": ['gte', 'lte', 'exact', 'gt', 'lt'],
    }
    search_fields = ["notification_type"]
    ordering_fields = ["updated_at", "created_at"]
    order = ["-updated_at", "-created_at"]
    ordering = ["-updated_at", "-created_at"]
    parser_classes = [FormParser, MultiPartParser, JSONParser]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return NotificationDetailSerializer
        return NotificationSerializer
