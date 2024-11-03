from django.db import models
from django.utils.translation import gettext_lazy as _

from mopito_project.core.models import BaseModel

# Create your models here.

class BaseActors(BaseModel):
    """
    Base model of staff entities (WorkManager and Guarantor)
    """
    Sex = (("M", "MALE"), ("F", "FEMALE"))

    first_name = models.CharField(_("first_name"), max_length=50, null=True, blank=True)
    last_name = models.CharField(_("first_name"), max_length=50, null=True, blank=True)
    gender = models.CharField(_("gender"), max_length=10, choices=Sex, default="M")
    code = models.CharField(_("code"), max_length=50, null=False, blank=False, default="1234")
    dob = models.DateTimeField(_("dob"), default=None, blank=True, null=True)
    profile_picture_file = models.FileField(
        _("profile_picture_file"), null=True, blank=True, upload_to="profile_picture/%Y/%m/%D/"
    )
    email = models.CharField(_("email"), max_length=100, null=True, blank=True)

    class Meta:
        abstract = True

class Patients(BaseModel):
    height = models.FloatField(_("height"), null=True, blank=True)
    weight = models.FloatField(_("weight"), null=True, blank=True)
    class Meta:
        """
        the place to configure de class or entities
        """
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")
        ordering = ("created_at",)

    # def __str__(self):
    #     return f"{self.first_name} {self.last_name}"
    
# class Staffs(BaseModel):
#     staff_type = (
#     ("NURSE", "NURSE"), ("GENERALIST", "GENERALIST"), ("SPECIALIST", "SPECIALIST"), ("CASHIER", "CASHIER"))
#     type = models.CharField(_("type"), max_length=10, choices=staff_type, default="NURSE")
#     # h_unite = models.ForeignKey(
#     #     HUnite,
#     #     on_delete=models.CASCADE,
#     #     null=True,
#     #     blank=True,
#     #     related_name="staffs",
#     # )

#     class Meta:
#         """
#         the place to configure de class or entities
#         """
#         verbose_name = _("Staff")
#         verbose_name_plural = _("Staffs")
#         ordering = ("created_at",)
    
