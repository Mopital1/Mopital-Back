
from mopito_project.core.api.serializers import BaseSerializer
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
    PaymentMethod,
    Pricing
)
from mopito_project.users.models import Profile, User
from mopito_project.users.api.serializers import ProfileSerializer, UserSerializer
from rest_framework import serializers
from mopito_project.utils.functionUtils import enc_decrypt_permutation


class CreatePatientSerializer(BaseSerializer):
    class Meta:
        model = Patients
        fields = (
            "id",
            "height",
            "weight",
            "blood_group",
            "rhesus_factor",
            "hemoglobin",
            "patient_parent",
            "parent_relation_typ",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at",)

class MedicalFolderSerializer(BaseSerializer):
    class Meta:
        model = MedicalFolder
        fields = (
            "id",
            "medical_history",
            "ongoing_treatments",
            "patient",
            "recent_consultations_summary",
            "lifestyle_and_habits",
            "emergency_contact",
            "medical_folder_password",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at",)

class DocumentSerializer(BaseSerializer):
    class Meta:
        model = Document
        fields = (
            "id",
            "document_name",
            "document", 
            "medical_folder",
            "created_at",
            "updated_at",
        )

class MedicalFolderDetailSerializer(BaseSerializer):
    medical_folder_password = serializers.SerializerMethodField()
    documents = DocumentSerializer(many=True)
    class Meta:
        model = MedicalFolder
        fields = (
            "id",
            "medical_history",
            "ongoing_treatments",
            "patient",
            "recent_consultations_summary",
            "lifestyle_and_habits",
            "emergency_contact",
            "medical_folder_password",
            "documents",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at",)

    def get_medical_folder_password(self, obj):
        medical_folder_password = enc_decrypt_permutation(obj.medical_folder_password)
        return medical_folder_password

class PatientSerializer(BaseSerializer):
    first_name = serializers.CharField(source="user.profile.first_name")
    last_name = serializers.CharField(source="user.profile.last_name")
    email = serializers.EmailField(source="user.profile.email")
    class Meta:
        model = Patients
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "height",
            "weight",
            "blood_group",
            "rhesus_factor",
            "hemoglobin",
            "patient_parent",
            "parent_relation_typ",
            # "children",
            "created_at",
            "updated_at",

        )
        read_only_fields = ("id", "created_at", "updated_at",)

class UpdatePatientSerializer(BaseSerializer):
    gender = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    class Meta:
        model = Patients
        fields = (
            "id",
            "height",
            "weight",
            "blood_group",
            "rhesus_factor",
            "hemoglobin",
            "gender",
            "first_name",
            "last_name",
            # "patient_parent",
            # "parent_relation_typ",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at",)
    
    def update(self, instance, validated_data):
        instance.height = validated_data.get("height", instance.height)
        instance.weight = validated_data.get("weight", instance.weight)
        instance.blood_group = validated_data.get("blood_group", instance.blood_group)
        instance.rhesus_factor = validated_data.get("rhesus_factor", instance.rhesus_factor)
        instance.hemoglobin = validated_data.get("hemoglobin", instance.hemoglobin)
        # instance.patient_parent = validated_data.get("patient_parent", instance.patient_parent)
        # instance.parent_relation_typ = validated_data.get("parent_relation_typ", instance.parent_relation_typ)
        instance.user.profile.gender = validated_data.get("gender", instance.user.profile.gender)
        instance.user.profile.first_name = validated_data.get("first_name", instance.user.profile.first_name)
        instance.user.profile.last_name = validated_data.get("last_name", instance.user.profile.last_name)
        instance.user.profile.save()

        instance.save()
        return instance
    
class NearPatientSerializer(BaseSerializer):
    email = serializers.EmailField()
    gender = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    dob = serializers.DateField()
    class Meta:
        model = Patients
        fields = (
            "id",
            "first_name",
            "last_name",
            "dob",
            "height",
            "weight",
            "email",
            "gender",
            "parent_relation_typ",
            # "patient_parent",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at",)
    
    def validate(self, data):
        height = data.get("height")
        weight = data.get("weight")
        if height <= 0 or weight <= 0:
            raise serializers.ValidationError("Height and weight must be greater than 0")
        return data

class CountrySerializer(BaseSerializer):
    class Meta:
        model = Countries
        fields = (
            "id",
            "name",
            "code",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at",)

class UserProfileSerializer(BaseSerializer):
    profile = ProfileSerializer()
    
    class Meta:
        model = User
        fields = (
            "id", 
            "is_active", 
            #"email", 
            "user_typ",
            "profile",
            "created_at",
            "updated_at",
            )
        # extra_kwargs = {"password": {"write_only": True}}
# class PatientChildSerializer(BaseSerializer):
#     class Meta:
#         model = Profile
#         fields = (
#             "id",
#             ""
#             "created_at",
#             "updated_at",
#         )
#         read_only_fields = ("id", "created_at", "updated_at",)

class PatientDetailSerializer(BaseSerializer):
    # profile = ProfileSerializer(source="user.profile")
    user = UserProfileSerializer()
    children = serializers.SerializerMethodField(read_only=True)
    medical_folder = MedicalFolderDetailSerializer()
    # children = UserProfileSerializer(many=True)
    # patient_parent = UserProfileSerializer(source="patient_parent.user", read_only=True)
    class Meta:
        model = Patients
        fields = (
            "id",
            # "profile",
            "height",
            "weight",
            "rhesus_factor",
            "blood_group",
            "hemoglobin",
            "parent_relation_typ",
            "medical_folder",
            # "patient_parent",
            "children",
            "user",
            "created_at",
            "updated_at",
        )
    read_only_fields = ("id", "created_at", "updated_at",)

    def get_children(self, obj):
        children = obj.children.all()
        return PatientSerializer(children, many=True).data

class SpecialitySerializer(BaseSerializer):
    class Meta:
        model = Speciality
        fields = (
            "id",
            "name",
            "description",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at",)


class StaffSerializer(BaseSerializer):
    # 
    class Meta:
        model = Staffs
        fields = (
            "id",
            "type",
            "title",
            "presentation",
            "professional_card",
            "diploma",
            "created_at",
            "updated_at"
        )

class TimeSlotSerializer(BaseSerializer):
    class Meta:
        model = TimeSlots
        fields = (
            "id",
            "day_of_week",
            # "start_time",
            # "end_time",
            "open_time",
            "close_time",
            "staff",
            "is_available",
            "created_at",
            "updated_at"
        )
        read_only_fields = ("id", "created_at", "updated_at",)

    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     if user.user_typ == "STAFF":
    #         validated_data["staff"] = user.staff
    #     timeslot = TimeSlots.objects.create(**validated_data)
    #     return timeslot

class StaffPathSerializer(BaseSerializer):
    class Meta:
        model = StaffPath
        fields = (
            "id",
            "description",
            "start_year",
            "end_year",
            "path_type",
            "staff",
            "created_at",
            "updated_at"
        )
    read_only_fields = ("id", "created_at", "updated_at",)

class PaymentMethodSerializer(BaseSerializer):
    class Meta:
        model = PaymentMethod
        fields = (
            "id",
            "payment_type",
            "phone_number",
            "staff",
            "created_at",
            "updated_at"
        )
    read_only_fields = ("id", "created_at", "updated_at",)

class PricingSerializer(BaseSerializer):
    class Meta:
        model = Pricing
        fields = (
            "id",
            "amount",
            "pricing_type",
            "staff",
            "created_at",
            "updated_at"
        )
class StaffDetailSerializer(BaseSerializer):
    user = UserProfileSerializer()
    speciality = SpecialitySerializer()
    # time_slots = TimeSlotSerializer(many=True)
    time_slots = serializers.SerializerMethodField()
    # staff_paths = StaffPathSerializer(many=True)
    staff_paths = serializers.SerializerMethodField()
    # staff_pricing = PricingSerializer(many=True)
    staff_pricing = serializers.SerializerMethodField()
    # payment_methods = PaymentMethodSerializer(many=True)
    payment_methods = serializers.SerializerMethodField()
    class Meta:
        model = Staffs
        fields = (
            "id", 
            "type",
            "title",
            "presentation",
            "staff_paths",
            "professional_card",
            "diploma",
            "speciality",
            "staff_pricing",
            "time_slots",
            "user",
            "payment_methods",
            "created_at",
            "updated_at",
            )
        # extra_kwargs = {"password": {"write_only": True}}

    def get_time_slots(self, obj):
        time_slots = TimeSlots.objects.filter(staff=obj)
        time_slots_dict = {}
        for time_slot in time_slots:
            if time_slot.day_of_week not in time_slots_dict:
                time_slots_dict[time_slot.day_of_week] = []
            time_slots_dict[time_slot.day_of_week].append({
                "open_time": time_slot.open_time,
                "close_time": time_slot.close_time,
                "is_available": time_slot.is_available
            })
        return time_slots_dict
    
    def get_staff_paths(self, obj):
        staff_paths = StaffPath.objects.filter(staff=obj)
        staff_paths_dict = {}
        for staff_path in staff_paths:
            if staff_path.path_type not in staff_paths_dict:
                staff_paths_dict[staff_path.path_type] = []
            staff_paths_dict[staff_path.path_type].append({
                "description": staff_path.description,
                "start_year": staff_path.start_year,
                "end_year": staff_path.end_year,
                "is_active": staff_path.is_active
            })
        return staff_paths_dict
    
    def get_staff_pricing(self, obj):
        staff_pricing = Pricing.objects.filter(staff=obj)
        staff_pricing_dict = {}
        for pricing in staff_pricing:
            if pricing.pricing_type not in staff_pricing_dict:
                staff_pricing_dict[pricing.pricing_type] = []
            staff_pricing_dict[pricing.pricing_type].append({
                "amount": pricing.amount,
                "is_active": pricing.is_active
            })
        return staff_pricing_dict
    
    def get_payment_methods(self, obj):
        payment_methods = PaymentMethod.objects.filter(staff=obj)
        payment_methods_dict = {}
        for payment_method in payment_methods:
            if payment_method.payment_type not in payment_methods_dict:
                payment_methods_dict[payment_method.payment_type] = []
            payment_methods_dict[payment_method.payment_type].append({
                "phone_number": payment_method.phone_number,
                "is_active": payment_method.is_active
            })
        return payment_methods_dict
    
class TimeSlotSerializer(BaseSerializer):
    class Meta:
        model = TimeSlots
        fields = (
            "id",
            "day_of_week",
            # "start_time",
            # "end_time",
            "open_time",
            "close_time",
            "staff",
            "is_available",
            "created_at",
            "updated_at"
        )
        read_only_fields = ("id", "created_at", "updated_at",)

    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     if user.user_typ == "STAFF":
    #         validated_data["staff"] = user.staff
    #     timeslot = TimeSlots.objects.create(**validated_data)
    #     return timeslot

class TimeSlotDetailSerializer(BaseSerializer):
    staff = StaffDetailSerializer()
    class Meta:
        model = TimeSlots
        fields = (
            "id",
            # "start_time",
            # "end_time",
             "open_time",
            "close_time",
            "is_available",
            "staff",
            "created_at",
            "updated_at"
        )
        read_only_fields = ("id", "created_at", "updated_at",)

class SubscriptionSerializer(BaseSerializer):
    class Meta:
        model = Subscriptions
        fields = (
            "id",
            "plan",
            "price",
            "staff",
            "start_date",
            "end_date",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at",)

class SubscriptionDetailSerializer(BaseSerializer):
    staff = StaffDetailSerializer()
    class Meta:
        model = Subscriptions
        fields = (
            "id",
            "plan",
            "price",
            "start_date",
            "end_date",
            "staff",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at",)

class ClinicSerializer(BaseSerializer):
    class Meta:
        model = Clinics
        fields = (
            "id",
            "name",
            "description",
            "address",
            "phone_number",
            "email",
            "start_time",
            "end_time",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at",)

class ClinicDetailSerializer(BaseSerializer):
    staffs = StaffDetailSerializer(many=True)
    class Meta:
        model = Clinics
        fields = (
            "id",
            "name",
            "description",
            "address",
            "phone_number",
            "email",
            "start_time",
            "end_time",
            "staffs",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at",)