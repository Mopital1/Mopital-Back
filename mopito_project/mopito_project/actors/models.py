from django.db import models
from django.utils.translation import gettext_lazy as _

from mopito_project.core.models import BaseModel

# Create your models here.


class Patients(BaseModel):
    # patient blood group enum
    bld_group = (
        ("AB", "AB"),
        ("A", "A"),
        ("B", "B"),
        ("O", "O"),)
    # patient rhesus factor enum
    rh_factor = (
        ("POSITIVE", "POSITIVE"),
        ("NEGATIVE", "NEGATIVE"),)
    patient_hemoglobin = (
        ("AA", "AA"),
        ("AS", "AS"),
        ("SS", "SS"))
    relation_typ = (
        ("CHILD", "CHILD"),
        ("PARENT", "PARENT"),
        ("BROTHER/SISTER", "BROTHER/SISTER"),
        ("GRANDPARENT", "GRANDPARENT"),
        ("OTHER", "OTHER"),
    )

    height = models.FloatField(_("height"), null=True, blank=True)
    weight = models.FloatField(_("weight"), null=True, blank=True)
    blood_group = models.CharField(_("blood_group"), 
                                     max_length=10, 
                                     null=True, 
                                     blank=True,
                                     choices=bld_group)
    rhesus_factor = models.CharField(_("rhesus_factor"),
                                        max_length=10,
                                        null=True,
                                        blank=True,
                                        choices=rh_factor,)
    hemoglobin = models.CharField(_("hemoglobin"),
                                    max_length=10,
                                    null=True,
                                    blank=True,
                                    choices=patient_hemoglobin)
    patient_parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    parent_relation_typ = models.CharField(_("parent_relation_typ"),
                                            max_length=30,
                                            choices=relation_typ,
                                            null=True,
                                            blank=True)

    class Meta:
        """
        the place to configure de class or entities
        """
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")
        ordering = ("-created_at",)

    # def __str__(self):
    #     return f"{self.first_name} {self.last_name}"
    
class Speciality(BaseModel):
    name = models.CharField(_("name"), max_length=200)
    description = models.TextField(_("description"))

    
class Staffs(BaseModel):
    staff_type = (
    ("NURSE", "NURSE"), ("GENERALIST", "GENERALIST"), ("SPECIALIST", "SPECIALIST"), ("CASHIER", "CASHIER"))
    type = models.CharField(_("type"), max_length=10, choices=staff_type, default="SPECIALIST")
    speciality = models.ForeignKey(Speciality, 
                                   on_delete=models.CASCADE, 
                                   related_name="staffs",
                                   null=True)


    class Meta:
        """
        the place to configure de class or entities
        """
        verbose_name = _("Staff")
        verbose_name_plural = _("Staffs")
        ordering = ("-created_at",)


class TimeSlots(BaseModel):
    start_time = models.DateTimeField(_("start_time"))
    end_time = models.DateTimeField(_("end_time"))
    staff = models.ForeignKey(Staffs, on_delete=models.CASCADE, related_name="time_slots")
    is_available = models.BooleanField(_("is_available"), default=True)

    class Meta:
        """
        the place to configure de class or entities
        """
        verbose_name = _("TimeSlot")
        verbose_name_plural = _("TimeSlots")
        ordering = ("-created_at",)
    
class Subscriptions(BaseModel):
    subscription_type = (
        ("MONTHLY", "MONTHLY"),
        ("QUARTERLY", "QUARTERLY"),
        ("YEARLY", "YEARLY"),
    )
    plan = models.CharField(_("plan"), max_length=10, choices=subscription_type, default="MONTHLY")
    price = models.FloatField(_("price"), default=0.0)
    staff = models.ForeignKey(Staffs, on_delete=models.CASCADE, related_name="subscriptions")
    start_date = models.DateTimeField(_("start_date"))
    end_date = models.DateTimeField(_("end_date"))
    has_expired = models.BooleanField(_("has_expired"), default=False)
    

    class Meta:
        """
        the place to configure de class or entities
        """
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")
        ordering = ("-created_at",)

class Countries(BaseModel):
    name = models.CharField(_("name"), max_length=200)
    code = models.CharField(_("code"), max_length=10)

    class Meta:
        """
        the place to configure de class or entities
        """
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
        ordering = ("-created_at",)

class Clinics(BaseModel):
    name = models.CharField(_("name"), max_length=200)
    description = models.TextField(_("description"))
    address = models.TextField(_("address"))
    phone_number = models.CharField(_("phone_number"), max_length=20)
    email = models.EmailField(_("email"), max_length=254)
    start_time = models.TimeField(_("start_time"))
    end_time = models.TimeField(_("end_time"))
    staffs = models.ManyToManyField(Staffs, related_name="clinics")

    class Meta:
        """
        the place to configure de class or entities
        """
        verbose_name = _("Clinical")
        verbose_name_plural = _("Clinicals")
        ordering = ("-created_at",)

