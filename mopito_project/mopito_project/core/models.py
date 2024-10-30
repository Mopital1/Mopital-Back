import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModelUser(models.Model):
    """
    Base class for all models in the application.
    """
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name=_("created by"),
        related_name="+",
        null=True,
        blank=True,
    )

    updated_by = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name=_("updated by"),
        related_name="+",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        _("update at"), auto_now=True, null=True, blank=True
    )

    is_active = models.BooleanField(
        _("is active"),
        default=True,
        help_text=_(
            "Designates whether this model should be treated as active or not."
        ),
    )

    class Meta:
        abstract = True


class BaseModel(BaseModelUser):
    """
    Base class for all models in the application.
    """
    id = models.UUIDField(_("id"), primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
