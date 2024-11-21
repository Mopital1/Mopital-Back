
from mopito_project.core.api.serializers import BaseSerializer
from mopito_project.actors.models import Clinics, Patients, Staffs, Subscriptions, TimeSlots
from mopito_project.users.models import Profile, User
from mopito_project.users.api.serializers import ProfileSerializer, UserSerializer


class PatientSerializer(BaseSerializer):
    class Meta:
        model = Patients
        fields = (
            "id",
            "height",
            "weight",
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
            "email", 
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
    user = UserProfileSerializer()
    children = PatientSerializer(many=True)
    class Meta:
        model = Patients
        fields = (
            "id",
            "height",
            "weight",
            "user",

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
            "created_at",
            "updated_at"
        )

class StaffDetailSerializer(BaseSerializer):
    user = UserProfileSerializer()
    class Meta:
        model = Staffs
        fields = (
            "id", 
            "type",
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