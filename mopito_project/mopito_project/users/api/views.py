# from rest_framework import status
# from rest_framework.decorators import action
# from rest_framework.mixins import ListModelMixin
# from rest_framework.mixins import RetrieveModelMixin
# from rest_framework.mixins import UpdateModelMixin
# from rest_framework.response import Response
# from rest_framework.viewsets import GenericViewSet

# from mopito_project.users.models import User

# from .serializers import UserSerializer


# class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#     lookup_field = "username"

#     def get_queryset(self, *args, **kwargs):
#         assert isinstance(self.request.user.id, int)
#         return self.queryset.filter(id=self.request.user.id)

#     @action(detail=False)
#     def me(self, request):
#         serializer = UserSerializer(request.user, context={"request": request})
#         return Response(status=status.HTTP_200_OK, data=serializer.data)

import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response

from mopito_project.core.api.views import BaseModelViewSet
from mopito_project.users.models import OTP
from mopito_project.users.api.serializers import (
    CreateUserSerializer,
    GroupSerializer,
    PasswordSerializer,
    PermissionSerializer,
    PhoneOTPAuthTokenSerializer,
    PhoneSerializer,
    SelfPasswordSerializer,
    UserDetailSerializer,
    UserSerializer, TokenObtainLifetimeSerializer, TokenRefreshLifetimeSerializer, 
     GroupDetailSerializer,
)
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.tokens import RefreshToken
from mopito_project.users.api.prevents import UserLoginRateThrottle
# from hemodialyse.users.models import VisibilityGroup
from mopito_project.utils.getUser import get_user_name

User = get_user_model()
logger_users = logging.getLogger('users_logger')

class UserViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    BaseModelViewSet,
):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["email", "user_typ", "is_active"]
    search_fields = ["email", "user_typ", ]
    ordering_fields = ["-updated_at", "-created_at", "email", ]
    ordering = ["-updated_at", "-created_at", "user_typ"]

    def get_serializer_class(self):
        if (
            self.action == "create"
            or self.action == "update"
            or self.action == "partial_update"
        ):
            return CreateUserSerializer

        if self.action == "retrieve" or self.action == "list":
            return UserDetailSerializer

        if self.action == "set-password":
            return PasswordSerializer

        if self.action == "set-my-password":
            return SelfPasswordSerializer

        return UserSerializer

    @action(detail=False, methods=["GET"])
    def me(self, request):
        if request.method == "GET":
            serializer = UserDetailSerializer(
                request.user, context={"request": request}
            )
            return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=["PUT"], url_path="set-my-password")
    def set_my_password(self, request):
        username = self.request.user.email
        serializer = SelfPasswordSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            logger_users.info(f'User {username} set is password')
            return Response(status=status.HTTP_200_OK, data={})
        logger_users.error(f'User {username} can not set is password')
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    @action(detail=True, methods=["PUT"], url_path="set-password")
    def set_user_password(self, request, *args, **kwargs):
        serializer = PasswordSerializer(
            self.get_object(), data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

class ObtainPhoneOTPAuthToken(TokenViewBase):
       def get_serializer_class(self):
              return PhoneOTPAuthTokenSerializer

       def post(self, request, *args, **kwargs):
           serializer = PhoneOTPAuthTokenSerializer(data=request.data)
           serializer.is_valid(raise_exception=True)
           user = serializer.validated_data['user']
           refresh = RefreshToken.for_user(user)
           return Response({
               'refresh': str(refresh),
               'access': str(refresh.access_token),
           }, status=status.HTTP_200_OK)

class SendOTPView(TokenViewBase):
       def get_serializer_class(self):
           return PhoneSerializer

       def post(self, request, *args, **kwargs):
        #    phone_number = request.data.get('phone_number')
           serializer = PhoneSerializer(data=request.data)
           serializer.is_valid(raise_exception=True)
           phone_number = serializer.validated_data['phone_number']
           try:
               user = User.objects.get(profile__phone_number=phone_number)
               otp_instance = OTP.objects.create(user=user)
            #    send_otp(phone_number, otp_instance.otp)
               return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
           except User.DoesNotExist:
               return Response({'error': 'User with this phone number does not exist'}, status=status.HTTP_400_BAD_REQUEST)

class TokenObtainPairView(TokenViewBase):
    """
        Return JWT tokens (access and refresh) for specific user based on username and password.
    """
    # throttle_classes = (UserLoginRateThrottle,)
    serializer_class = TokenObtainLifetimeSerializer


class TokenRefreshView(TokenViewBase):
    """
        Renew tokens (access and refresh) with new expire time based on specific user's access token.
    """
    serializer_class = TokenRefreshLifetimeSerializer


class PermissionViewSet(BaseModelViewSet, ListModelMixin):
    """
    ViewSet for listing permissions.
    """

    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["name", "codename"]
    search_fields = ["name", "codename"]
    ordering_fields = ["name", "codename"]


class GroupViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    BaseModelViewSet,
):
    """
    ViewSet for creating, reading, updating and deleting groups.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["name", ]
    search_fields = ["name", ]
    ordering_fields = ["name", ]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return GroupDetailSerializer
        return GroupSerializer
