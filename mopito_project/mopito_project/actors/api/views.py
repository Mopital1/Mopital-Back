from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework import filters, mixins, status
from django.db import transaction
from django.db.models import Q, Case, When, Value, IntegerField
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser  
from mopito_project.core.api.views import BaseModelViewSet
from mopito_project.actors.models import (
    Clinics, 
    Countries, 
    Patients, 
    Speciality, 
    Staffs, 
    Subscriptions, 
    TimeSlots, 
    MedicalFolder, 
    Document, 
    StaffPath,
    Pricing,
    PaymentMethod
)
from actors.api.serializers import (
    ClinicDetailSerializer, 
    ClinicSerializer, 
    CountrySerializer,  
    NearPatientSerializer, 
    PatientDetailSerializer, 
    PatientSerializer, 
    SpecialitySerializer, 
    StaffDetailSerializer, 
    StaffSerializer, 
    SubscriptionDetailSerializer, 
    SubscriptionSerializer, 
    TimeSlotDetailSerializer, 
    TimeSlotSerializer, 
    UpdatePatientSerializer,
    MedicalFolderSerializer,
    MedicalFolderDetailSerializer,
    DocumentSerializer,
    StaffPathSerializer,
    PricingSerializer,
    PaymentMethodSerializer
)

from mopito_project.utils.functionUtils import get_user_email, remove_special_characters, enc_decrypt_permutation
from mopito_project.utils.sendsms import phoneNumberGenerator
from mopito_project.users.api.serializers import CompleteProfileSerializer, CreateProfileSerializer, ProfileSerializer
from mopito_project.users.models import Profile, User
from mopito_project.actors.api.serializers import CreatePatientSerializer
# from mopito_project.background_jobs.tasks import send_otp_to_user


class MedicalFolderViewSet(BaseModelViewSet, mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.CreateModelMixin):
    queryset = MedicalFolder.objects.filter(is_active=True)
    serializer_class = MedicalFolderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "patient_id": ['exact'],
        "patient__user__profile__first_name": ['exact', 'icontains'],
        "updated_at": ['gte', 'lte', 'exact', 'gt', 'lt'],
        "created_at": ['gte', 'lte', 'exact', 'gt', 'lt']
    }
    search_fields = ["patient__user__profile__first_name"]
    ordering_fields = ["updated_at", "created_at"]
    ordering = ["-updated_at", "-created_at"]
    parser_classes = [FormParser, MultiPartParser, JSONParser]

    # def get_queryset(self):
    #     user = self.request.user
    #     # send_otp_to_user(repeat=86400)
    #     if user.user_typ == "PATIENT":
    #         return MedicalFolder.objects.filter(patient=user.patient)
    #     return MedicalFolder.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return MedicalFolderDetailSerializer
        return MedicalFolderSerializer
    """
     @action(detail=False, methods=["post"])
    def add_near_patient(self, request, *args, **kwargs):
    """
    @action(detail=True, methods=["post"])
    def verify_medical_folder_password(self, request, *args, **kwargs):
        """
        Verify if the provided password for the medical folder is correct or not.
        """
        # medical_folder = MedicalFolder.objects.get(id=medical_folder_id)
        medical_folder = self.get_object()
        password = request.data.get('password')
        encrypt_pass = enc_decrypt_permutation(password)
        if not medical_folder.medical_folder_password == encrypt_pass:
            return Response({"msg": "Ok"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Password is not correct"}, status=status.HTTP_400_BAD_REQUEST)
class StaffPathViewSet(BaseModelViewSet, mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.CreateModelMixin):
    queryset = StaffPath.objects.filter(is_active=True)
    serializer_class = StaffPathSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        # "patient__user__profile__first_name": ['exact', 'icontains'],
        "staff_id": ['exact'],
        "path_type": ['exact'],
        "description": ['exact', 'icontains'],
        "start_year": ['gte', 'lte', 'exact', 'gt', 'lt'],
        "end_year": ['gte', 'lte', 'exact', 'gt', 'lt'],
        "updated_at": ['gte', 'lte', 'exact', 'gt', 'lt'],
        "created_at": ['gte', 'lte', 'exact', 'gt', 'lt']
    }
    search_fields = ["description"]
    ordering_fields = ["updated_at", "created_at"]
    ordering = ["-updated_at", "-created_at"]
    parser_classes = [FormParser, MultiPartParser, JSONParser]

class PaymentMethodViewSet(BaseModelViewSet, mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.CreateModelMixin):
    queryset = PaymentMethod.objects.filter(is_active=True)
    serializer_class = PaymentMethodSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "staff_id": ['exact'],
        "payment_type": ['exact'],
        "updated_at": ['gte', 'lte', 'exact', 'gt', 'lt'],
        "created_at": ['gte', 'lte', 'exact', 'gt', 'lt']

    }
    search_fields = ["phone_number"]
    ordering_fields = ["updated_at", "created_at"]
    ordering = ["-updated_at", "-created_at"]
    parser_classes = [FormParser, MultiPartParser, JSONParser]

class PricingViewSet(BaseModelViewSet, mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.CreateModelMixin):
    queryset = Pricing.objects.filter(is_active=True)
    serializer_class = PricingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "staff_id": ['exact'],
        "pricing_type": ['exact'],
        "updated_at": ['gte', 'lte', 'exact', 'gt', 'lt'],
        "created_at": ['gte', 'lte', 'exact', 'gt', 'lt']
    }
    search_fields = ["pricing_type", "amount"]
    ordering_fields = ["updated_at", "created_at"]
    ordering = ["-updated_at", "-created_at"]
    parser_classes = [FormParser, MultiPartParser, JSONParser]

class DocumentViewSet(BaseModelViewSet, mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.CreateModelMixin):
    queryset = Document.objects.filter(is_active=True)
    serializer_class = DocumentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "document_name": ['exact', 'icontains'],
        "medical_folder_id": ['exact'],
        "updated_at": ['gte', 'lte', 'exact', 'gt', 'lt'],
        "created_at": ['gte', 'lte', 'exact', 'gt', 'lt']

    }
    search_fields = ["document_name"]
    ordering_fields = ["updated_at", "created_at"]
    ordering = ["-updated_at", "-created_at"]
    parser_classes = [FormParser, MultiPartParser, JSONParser]



class PatientViewSet(BaseModelViewSet, mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.CreateModelMixin,):
    queryset = Patients.objects.filter(is_active=True)
    serializer_class = PatientSerializer
    # permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "user__id": ['exact'],
        "user__profile_id": ['exact'],
        "user__profile__first_name": ['exact', 'contains'],
        "user__profile__phone_number": ['exact', 'contains'],
        "patient_parent_id": ['exact'],
        "parent_relation_typ": ['exact'],
        "updated_at": ['gte', 'lte', 'exact', 'gt', 'lt'],
        "created_at": ['gte', 'lte', 'exact', 'gt', 'lt']
    }

    search_fields = ["user__profile__last_name", "user__profile__first_name"]
    ordering_fields = ["updated_at", "created_at"]
    ordering = ["-updated_at", "-created_at"]

    # def get_queryset(self):
    #     user = self.request.user
    #     # send_otp_to_user(repeat=86400)
    #     if user.user_typ == "PATIENT":
    #         # return Patients.objects.filter(id=user.patient.id)
    #         return Patients.objects.filter(patient_parent_id=user.patient.id)
    #     return Patients.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return PatientDetailSerializer
        if self.action == "create":
            return CreatePatientSerializer
        if self.action == "update" or self.action == "partial_update":
            return UpdatePatientSerializer
        if self.action == "add_near_patient":
            return NearPatientSerializer
        return PatientSerializer
    
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance = self.get_object()
            if not instance:
                return Response(
                    {"detail": "Patient non trouvé"},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            
            with transaction.atomic():  # Ajout d'une transaction atomique
                # Mise à jour des champs du patient
                validated_data = serializer.validated_data
                patient_fields = ['height', 'weight', 'blood_group', 'rhesus_factor', 'hemoglobin']
                for field in patient_fields:
                    setattr(instance, field, validated_data.get(field, getattr(instance, field)))

                # Mise à jour du medical folder password
                medical_folder_password = validated_data.get("medical_folder_password")
                if medical_folder_password and hasattr(instance, 'medical_folder') and instance.medical_folder:
                    instance.medical_folder.medical_folder_password = enc_decrypt_permutation(medical_folder_password)
                    instance.medical_folder.save()

                # Mise à jour du profil utilisateur
                if hasattr(instance, 'user') and hasattr(instance.user, 'profile'):
                    profile = instance.user.profile
                    profile_fields = ['gender', 'first_name', 'last_name']
                    for field in profile_fields:
                        setattr(profile, field, validated_data.get(field, getattr(profile, field)))
                    profile.save()

                instance.save()
            
            return Response(serializer.data)

        except Patients.DoesNotExist:
            return Response(
                {"detail": "Patient non trouvé"},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
                return Response(
                    {"detail": f"Erreur lors de la mise à jour du patient : {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
    
    @action(detail=False, methods=["post"])
    def add_near_patient(self, request, *args, **kwargs):
        serializer = NearPatientSerializer(data=request.data)
        user = self.request.user
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        email = serializer.validated_data.get("email", None)
        gender = serializer.validated_data.get("gender", None)
        height = serializer.validated_data.get("height", None)
        weight = serializer.validated_data.get("weight", None)
        dob = serializer.validated_data.get("dob")
        parent_relation_typ = serializer.validated_data.get("parent_relation_typ", None)
        first_name = remove_special_characters(serializer.validated_data.get("first_name")) 
        last_name = remove_special_characters(serializer.validated_data.get("last_name"))
        phone_number = phoneNumberGenerator()
        # if email is None:
        #     email = f"{phone_number}@mopito.com"
        # username = email.split("@")[0]
        print("user", user)
        print("user patient", user.patient)
        if user.patient is None:
            return Response({"error": "You are not a patient"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                profile = Profile.objects.create(
                    # username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    dob=dob,
                    phone_number=phone_number,
                    gender=gender
                )
                patient = Patients.objects.create(
                    patient_parent_id=user.patient.id,
                    parent_relation_typ=parent_relation_typ,
                    height=height,
                    weight=weight,
                )
                
                new_user = User.objects.create(
                    patient_id=patient.id,
                    profile_id=profile.id,
                    email=get_user_email(first_name, last_name),
                    user_typ="PATIENT"
                )
                return Response({
                    "profile": profile.id,
                    "patient": patient.id
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SpecialityViewSet(BaseModelViewSet, mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.CreateModelMixin):
    queryset = Speciality.objects.filter(is_active=True)
    serializer_class = SpecialitySerializer

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

    search_fields = ["user__profile__last_name", "user__profile__first_name", "user__profile__city", "speciality__name"]
    ordering_fields = ["updated_at", "created_at"]
    ordering = ["-updated_at", "-created_at"]

    def get_queryset(self):
       user = self.request.user
       base_queryset = Staffs.objects.filter(is_active=True)
       if user.user_typ == "PATIENT" and user.profile.city:
           # Annotate queryset with priority field
           return base_queryset.annotate(
               priority=Case(
                   When(user__profile__city__iexact=user.profile.city, then=Value(1)),
                   default=Value(2),
                   output_field=IntegerField(),
               )
           ).order_by('priority', '-updated_at')
       
       return base_queryset


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
        "close_time": ['gte', 'lte', 'exact', 'gt', 'lt'],
        "open_time": ['gte', 'lte', 'exact', 'gt', 'lt'],
        "day_of_week": ['exact']
        # "updated_at": ['gte', 'lte', 'exact', 'gt', 'lt'],
        # "created_at": ['gte', 'lte', 'exact', 'gt', 'lt']
    }
    search_fields = ["staff__user__profile__first_name", "day_of_week"]
    ordering_fields = ["updated_at", "created_at"]
    ordering = ["-updated_at", "-created_at"]

    def get_serializer_class(self):
        if self.action == "retrieve":
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

class CountryViewSet(BaseModelViewSet, mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.CreateModelMixin,):
        queryset = Countries.objects.filter(is_active=True)
        serializer_class = CountrySerializer
        filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
        filterset_fields = {
            "name": ['exact', 'contains'],
            "code": ['exact', 'contains'],
            "updated_at": ['gte', 'lte', 'exact', 'gt', 'lt'],
            "created_at": ['gte', 'lte', 'exact', 'gt', 'lt']
        }
        search_fields = ["name", "iso_code", "phone_code"]
        ordering_fields = ["updated_at", "created_at", "name"]
        ordering = ["-updated_at", "-created_at"]
    
        # def get_serializer_class(self):
        #     if self.action == "list" or self.action == "retrieve":
        #         return CountryDetailSerializer
        #     return CountrySerializer

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
    search_fields = ["first_name", "last_name"]
    ordering_fields = ["updated_at", "created_at"]
    ordering = ["-updated_at", "-created_at"]
    permission_classes = [AllowAny]
    parser_classes = [FormParser, MultiPartParser, JSONParser]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateProfileSerializer
        if self.action == "complete_profile":
            return CompleteProfileSerializer
        return ProfileSerializer

    @action(detail=False, methods=["post"])
    def complete_profile(self, request, *args, **kwargs):
        serializer = CompleteProfileSerializer(data=request.data)
        user = self.request.user
        
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        
        try:
            with transaction.atomic():
                patient = user.patient
                profile = user.profile
                
                if not patient or not profile:
                    return Response(
                        {"error": "Patient or Profile not found"}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                # Update profile
                profile.email = serializer.validated_data.get("email", None)
                profile.country = serializer.validated_data.get("country", None)
                profile.city = serializer.validated_data.get("city", None)
                profile.quarter = serializer.validated_data.get("quarter", None)
                profile.save()

                # Update patient
                patient.height = serializer.validated_data.get("height", 0)
                patient.weight = serializer.validated_data.get("weight", 0)
                patient.save()

            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )  

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