from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager as BaseUserManager
from django.core.mail import send_mail
import random
import pytz
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from mopito_project.core.models import BaseModel, BaseModelUser
from mopito_project.actors.models import Patients, Staffs
# Staffs



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError("The given email address must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Email and password are required. Other fields are optional.
    """
    email = models.EmailField(
        _("email address"),
        max_length=254,
        unique=True,
        error_messages={"unique": _("A user with that email address already exists.")},
    )
    
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin " "site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)


    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the full name for the user...
        """
        return self.email

    def get_short_name(self):
        """Return the short name for the user."""
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Email this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Profile(BaseModel):
    """
    class for user profile
    """
    Sex = (("M", "MALE"), ("F", "FEMALE"))
    
    phone_number = models.CharField(
        _("phone_number"), 
        max_length=20, 
        unique=True,
        null=True,
        blank=True,
        error_messages={"unique": _("A user with that phone number already exists.")},
        )
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        error_messages={"unique": _("A user with that username already exists.")},
    )
    first_name = models.CharField(_("first_name"), max_length=50, null=True, blank=True)
    last_name = models.CharField(_("first_name"), max_length=50, null=True, blank=True)
    gender = models.CharField(_("gender"), max_length=10, choices=Sex, default="M")
    code = models.CharField(_("code"), max_length=50, null=True, blank=True)
    dob = models.DateTimeField(_("dob"), default=None, blank=True, null=True)
    profile_picture_file = models.FileField(
        _("profile_picture_file"), null=True, blank=True, upload_to="profile_picture/%Y/%m/%D/"
    )

class User(AbstractUser, BaseModelUser):
    """
    Users within the Django authentication system are represented by this
    model.
    Email and password are required. Other fields are optional.
    """

    UserTyp = (
        ("PATIENT", "PATIENT"),
        ("STAFF", "STAFF"),
        ("ADMIN", "ADMIN"),
    )

    user_typ = models.CharField(_("user_typ"), max_length=20, choices=UserTyp, default="ADMIN")
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="user",
    )

    # est rattaché ou pas à une clinique

    patient = models.OneToOneField(
        Patients,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="user",
    )

    staff = models.OneToOneField(
        Staffs,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="user",
    )

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"


class OTP(TimeStampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("user"),
        related_name="otps"
    )
    used = models.BooleanField(_("used"), default=False)
    otp = models.CharField(max_length=6)
    used = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = str(random.randint(10000, 99999))
        # super().save(*args, **kwargs)
        self.created = datetime.now()
        super(TimeStampedModel, self).save(*args, **kwargs)


    def is_valid(self, obj):
        # Add logic to check if OTP is still valid (e.g., not expired)
        # return True
        otp = obj
        if otp.used:
            return False
        expired_at = otp.created + timedelta(minutes=settings.VALID_TOKEN_TIME)
        now = pytz.utc.localize(datetime.now())

        if now < expired_at:
            return True

        otp.used = True
        otp.save()

        return False
   


# class User(AbstractUser):
#     """
#     Default custom user model for Mopito Project.
#     If adding fields that need to be filled at user signup,
#     check forms.SignupForm and forms.SocialSignupForms accordingly.
#     """

#     # First and last name do not cover name patterns around the globe
#     name = CharField(_("Name of User"), blank=True, max_length=255)
#     first_name = None  # type: ignore[assignment]
#     last_name = None  # type: ignore[assignment]

#     def get_absolute_url(self) -> str:
#         """Get URL for user's detail view.

#         Returns:
#             str: URL for user detail.

#         """
#         return reverse("users:detail", kwargs={"username": self.username})
