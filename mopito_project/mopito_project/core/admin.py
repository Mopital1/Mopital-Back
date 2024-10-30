from django.contrib import admin
from django.utils.timezone import datetime


class BaseModelAdmin(admin.ModelAdmin):
    """
    Base admin class for all models in the application.
    """

    readonly_fields = ("created_at", "created_by", "updated_at", "updated_by")

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_at = datetime.now()
            obj.updated_by = request.user
        else:
            obj.created_at = datetime.now()
            obj.created_by = request.user

        super().save_model(request, obj, form, change)
