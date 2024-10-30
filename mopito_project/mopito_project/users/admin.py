# from allauth.account.decorators import secure_admin_login
# from django.conf import settings
# from django.contrib import admin
# from django.contrib.auth import admin as auth_admin
# from django.utils.translation import gettext_lazy as _

# from .forms import UserAdminChangeForm
# from .forms import UserAdminCreationForm
# from .models import User

# if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
#     # Force the `admin` sign in process to go through the `django-allauth` workflow:
#     # https://docs.allauth.org/en/latest/common/admin.html#admin
#     admin.autodiscover()
#     admin.site.login = secure_admin_login(admin.site.login)  # type: ignore[method-assign]


# @admin.register(User)
# class UserAdmin(auth_admin.UserAdmin):
#     form = UserAdminChangeForm
#     add_form = UserAdminCreationForm
#     fieldsets = (
#         (None, {"fields": ("username", "password")}),
#         (_("Personal info"), {"fields": ("name", "email")}),
#         (
#             _("Permissions"),
#             {
#                 "fields": (
#                     "is_active",
#                     "is_staff",
#                     "is_superuser",
#                     "groups",
#                     "user_permissions",
#                 ),
#             },
#         ),
#         (_("Important dates"), {"fields": ("last_login", "date_joined")}),
#     )
#     list_display = ["username", "name", "is_superuser"]
#     search_fields = ["name"]

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

# from hemodialyse.core.admin import BaseModelAdmin
from mopito_project.core.admin import BaseModelAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin, BaseModelAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    # "visibility_groups",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("pk", "email", "created_at", "created_by", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "created_at")
    search_fields = ("email",)
    ordering = ("email", "created_at")
    date_hierarchy = "created_at"
