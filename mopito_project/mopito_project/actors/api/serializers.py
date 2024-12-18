
from mopito_project.core.api.serializers import BaseSerializer
from mopito_project.actors.models import Clinics, Countries, Patients, Speciality, Staffs, Subscriptions, TimeSlots
from mopito_project.users.models import Profile, User
from mopito_project.users.api.serializers import ProfileSerializer, UserSerializer
from rest_framework import serializers

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
            "created_at",
            "updated_at"
        )

class StaffDetailSerializer(BaseSerializer):
    user = UserProfileSerializer()
    speciality = SpecialitySerializer()
    class Meta:
        model = Staffs
        fields = (
            "id", 
            "type",
            "title",
            "speciality",
            "user",
            "created_at",
            "updated_at",
            )
        # extra_kwargs = {"password": {"write_only": True}}

class TimeSlotSerializer(BaseSerializer):
    class Meta:
        model = TimeSlots
        fields = (
            "id",
            "start_time",
            "end_time",
            "is_available",
            "created_at",
            "updated_at"
        )
        read_only_fields = ("id", "created_at", "updated_at",)

class TimeSlotDetailSerializer(BaseSerializer):
    staff = StaffDetailSerializer()
    class Meta:
        model = TimeSlots
        fields = (
            "id",
            "start_time",
            "end_time",
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