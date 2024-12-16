# from rest_framework import serializers

# from mopito_project.users.models import User


# class UserSerializer(serializers.ModelSerializer[User]):
#     class Meta:
#         model = User
#         fields = ["username", "name", "url"]

#         extra_kwargs = {
#             "url": {"view_name": "api:user-detail", "lookup_field": "username"},
#         }

import logging

from django.contrib.auth.models import Group, Permission
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import transaction

# from hemodialyse.core.api.serializers import BaseSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from mopito_project.core.api.serializers import BaseSerializer
from mopito_project.utils.functionUtils import get_user_email
from mopito_project.utils.sendsms import send_otp
from mopito_project.utils import randomize_digit_char
from mopito_project.users.models import OTP, Profile, User
from mopito_project.actors.models import Patients, Staffs, Speciality
from mopito_project.actors.models import Countries

# from ..models import User, VisibilityGroup
# from ...h_centers.api.serializers import HUniteSerializers
# from ...utils.randomize_digit_char import randomize_digit_char


def generate_user_code():
    """"""
    user_code = randomize_digit_char(N=4)
    exist_user = User.objects.filter(is_active=True, user_code=user_code).exists()
    if exist_user:
        return generate_user_code()
    return user_code


# class VisibilityGroupSerializer(BaseSerializer):
#     class Meta:
#         model = VisibilityGroup
#         fields = ("id", "name", "code", "slug", "description", "h_unite")


# class VisibilityDetailGroupSerializer(BaseSerializer):
#     h_unite = HUniteSerializers(many=True, read_only=True)

#     class Meta:
#         model = VisibilityGroup
#         fields = ("id", "name", "code", "slug", "description", "h_unite")


class PermissionSerializer(BaseSerializer):
    """
    Serializer for Permission.
    """

    code = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = ["id", "name", "code"]

    def get_code(self, obj) -> str:
        return f"{obj.content_type.app_label}.{obj.codename}"


class GroupSerializer(BaseSerializer):
    """
    Serializer for Group.
    """

    class Meta:
        model = Group
        fields = ["id", "name", "permissions"]


class GroupDetailSerializer(BaseSerializer):
    permissions = serializers.SerializerMethodField()
    """
    Serializer for Group.
    """

    class Meta:
        model = Group
        fields = ["id", "name", "permissions"]

    def get_permissions(self, obj):
        permissions = Permission.objects.filter(group=obj)
        return PermissionSerializer(permissions, many=True).data

class CreateProfileSerializer(BaseSerializer):
    user_typ = serializers.CharField(required=False, write_only=True)
    title = serializers.CharField(required=False, write_only=True)
    # staff_type = serializers.CharField(required=False, write_only=True)
    # speciality id is only for staff, and is uuid
    speciality_id = serializers.UUIDField(required=False, write_only=True)
    
    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "phone_number",
            "profile_picture_file",
            #"username",
            "user_typ",
            # "staff_type",
            "speciality_id",
            "title",
            "gender",
            "dob",
            )
    
    def validate(self, data):
        if not data.get('phone_number'):
            raise serializers.ValidationError("Phone number is required")
            
        if data.get("user_typ") == "STAFF":
            # if not data.get("staff_type"):
            #     raise serializers.ValidationError("Staff type is required for staff users")
            if not data.get("speciality_id"):
                raise serializers.ValidationError("Speciality is required for staff users")
            if not Speciality.objects.filter(id=data.get("speciality_id")).exists():
                raise serializers.ValidationError("Speciality does not exist")
        
        return data

    @transaction.atomic
    def create(self, validated_data):
        try:
            user_typ = validated_data.pop("user_typ", "PATIENT")
            # staff_type = validated_data.pop("staff_type", "GENERALIST")
            speciality_id = validated_data.pop("speciality_id", None)
            title = validated_data.pop("title", None)
            profile = Profile.objects.create(**validated_data)
            email = get_user_email(validated_data.get("first_name"), validated_data.get("last_name"))
            
            user = User.objects.create(
                profile_id=profile.id,
                user_typ=user_typ,
                email=email,
            )

            if user_typ == "PATIENT":
                patient = Patients.objects.create(height=0, weight=0)
                user.patient = patient
            elif user_typ == "STAFF":
                staff = Staffs.objects.create(speciality_id=speciality_id, title=title)
                user.staff = staff
            user.save()

            otp_instance = OTP.objects.create(user=user)
            otp_code = str(otp_instance.otp)
            send_otp(profile.phone_number, otp_code)
            
            return profile
            
        except Exception as e:
            raise serializers.ValidationError(f"Error creating profile: {str(e)}")
        
class CompleteProfileSerializer(BaseSerializer):
    # email = serializers.EmailField(required=False, write_only=True)
    height = serializers.FloatField(required=False, write_only=True)
    weight = serializers.FloatField(required=False, write_only=True)
    class Meta:
        model = Profile
        fields = (
            "email",
            "country",
            "city",
            "quarter",
            "height", 
            "weight",
            # "dob",
            # "gender"
        )

    # def validate(self, data):
    #     # Ajoutez ici des validations supplémentaires si nécessaire
    #     phone_number = data.get("phone_number")
    #     if not Profile.objects.filter(phone_number=phone_number).exists():
    #         raise serializers.ValidationError("Profile with this phone number does not exist.")
    #     return data

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


class ProfileSerializer(BaseSerializer):
    user_typ = serializers.CharField(required=False, write_only=True)
    country = CountrySerializer(read_only=True)
    # email = serializers.EmailField(required=False, write_only=True)
    class Meta:
        model = Profile
        fields = (
            "id",
            "phone_number",
            "email",
            #"username",
            "user_typ",
            "first_name",
            "last_name",
            "gender",
            "dob",
            "profile_picture_file",
            "code",
            "country",
            "city",
            "quarter",
            "created_at", 
            "updated_at"
        )
    read_only_fields = ("id", "created_at", "updated_at",)


    def create(self, validated_data):
        """
        Créer le profil et l'utilisateur associé
        """
        user_typ = validated_data.pop("user_typ", "PATIENT")
        # email = validated_data.pop("email", "default@gmail.com")
        password = validated_data.pop("password", None)
    
        # Créer le profil
        profile = Profile.objects.create(**validated_data)
    
        # Créer l'utilisateur
        user = User.objects.create(
            profile_id=profile.id,
            # email=email,
            user_typ=user_typ,
        )
        # Définir le mot de passe
        if password:
            user.set_password(password)
            user.save()
    
        return profile

class UserSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = (
            "id", "is_active", "email", "password", "user_typ")
        extra_kwargs = {"password": {"write_only": True}}

class CreateUserSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "is_active",
            "email",
            # "username",
            "user_typ",
            "password",
            "groups",
            "user_permissions",
            # "visibility_groups",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # Supprimer le champ "password" des données validées
        validated_data.pop('password', None)
        return super().update(instance, validated_data)

class UpdateUserSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "is_active",
            "email",
            "user_typ",
            "password",
            "groups",
            "user_permissions",
            # "visibility_groups",
        )
        extra_kwargs = {"password": {"write_only": True}}

class UserDetailSerializer(BaseSerializer):
    groups = GroupDetailSerializer(many=True)
    user_permissions = PermissionSerializer(many=True)
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "is_active",
            "email",
            "user_typ",
            "patient",
            "staff",
            "password",
            "user_permissions",
            "groups",
            "permissions",
            # "visibility_groups",

        )
        extra_kwargs = {"password": {"write_only": True}}
        depth = 1

    def get_permissions(self, obj):
        user_permissions = obj.get_user_permissions()
        groups = obj.groups.all()
        for group in groups:
            permissions = group.permissions.all()
            for permission in permissions:
                perm = f"{permission.content_type.app_label}.{permission.codename}"
                if perm not in user_permissions:
                    user_permissions.add(perm)
        return user_permissions


class SelfPasswordSerializer(BaseSerializer):
    old_password = serializers.CharField()

    class Meta:
        model = User
        fields = ("old_password", "password")
        extra_kwargs = {
            "password": {"write_only": True},
            "old_password": {"write_only": True},
        }

    def validate_old_password(self, value):
        if not self.context.get("request").user.check_password(value):
            raise ValidationError("Old password is invalid.")

        return value

    def save(self):
        user = self.context.get("request").user
        user.set_password(self.validated_data["password"])
        user.save()


class PasswordSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = ("password",)
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        user = self.instance
        user.set_password(self.validated_data["password"])
        user.save()


class TokenObtainLifetimeSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        # username = self.user.email
        refresh = self.get_token(self.user)
        data['lifetime'] = int(refresh.access_token.lifetime.total_seconds())
        return data


class TokenRefreshLifetimeSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken(attrs['refresh'])
        data['lifetime'] = int(refresh.access_token.lifetime.total_seconds())
        return data

class PhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        if not phone_number:
            raise serializers.ValidationError('Phone number is required')
        return attrs

class PhoneOTPAuthTokenSerializer(serializers.Serializer):
       phone_number = serializers.CharField()
       otp = serializers.CharField()

       def validate(self, attrs):
           phone_number = attrs.get('phone_number')
           otp = attrs.get('otp')

           try:
               user = User.objects.get(profile__phone_number=phone_number)  # Assuming phone_number is stored in a related profile model
           except User.DoesNotExist:
               raise serializers.ValidationError('User with this phone number does not exist')

           try:
               otp_instance = OTP.objects.get(user=user, otp=otp)
               if not otp_instance.is_valid():
                   raise serializers.ValidationError('Invalid or expired OTP')
           except OTP.DoesNotExist:
               raise serializers.ValidationError('Invalid OTP')

           attrs['user'] = user
           return attrs