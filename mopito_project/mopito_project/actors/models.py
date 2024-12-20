from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

from mopito_project.core.models import BaseModel
from mopito_project.utils.functionUtils import enc_decrypt_permutation

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

class MedicalFolder(BaseModel):
    medical_history = models.TextField(_("medical_history"), null=True, blank=True)
    ongoing_treatments = models.TextField(_("ongoing_treatments"), null=True, blank=True)
    patient = models.OneToOneField(Patients, on_delete=models.CASCADE, related_name="medical_folder")
    recent_consultations_summary = models.TextField(_("recent_consultations_summary"), null=True, blank=True)
    lifestyle_and_habits = models.TextField(_("lifestyle_and_habits"), null=True, blank=True)
    emergency_contact = models.TextField(_("emergency_contact"), null=True, blank=True)
    medical_folder_password = models.CharField(_("medical_folder_password"), max_length=6, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.medical_folder_password:
            self.medical_folder_password = enc_decrypt_permutation(self.medical_folder_password)
        super().save(*args, **kwargs)

    class Meta:
        """
        the place to configure de class or entities
        """
        verbose_name = _("MedicalFolder")
        verbose_name_plural = _("MedicalFolders")
        ordering = ("-created_at",)

class Document(BaseModel):
    document_name = models.CharField(_("document_name"), max_length=255, null=True, blank=True)
    document = models.FileField(_("document"), upload_to="documents/%Y/%m/%D/")
    medical_folder = models.ForeignKey(MedicalFolder, on_delete=models.CASCADE, related_name="documents", null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.document.size > 30 * 1024 * 1024:
            raise Exception("Document size exceeds 30 MB.")
        if not self.document.name.endswith('.pdf'):
            raise Exception("Document must be a PDF.")
        file_name, file_extension = self.document.name.rsplit('.', 1)
        self.document_name = f"{file_name.replace(' ','_')}_{uuid.uuid4().hex[:8]}.{file_extension}"
        super().save(*args, **kwargs)

    class Meta:
        """
        the place to configure de class or entities
        """
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")
        ordering = ("-created_at",)

class Speciality(BaseModel):
    name = models.CharField(_("name"), max_length=200)
    description = models.TextField(_("description"))

# class Pricing(BaseModel):

class Staffs(BaseModel):
    pro_title = (
        ("Dr", "Dr"),
        ("Pr", "Pr"),
)
    staff_type = (
    ("NURSE", "NURSE"), ("GENERALIST", "GENERALIST"), ("SPECIALIST", "SPECIALIST"), ("CASHIER", "CASHIER"))
    type = models.CharField(_("type"), max_length=10, choices=staff_type, default="SPECIALIST")
    speciality = models.ForeignKey(Speciality, 
                                   on_delete=models.CASCADE, 
                                   related_name="staffs",
                                   null=True)
    title = models.CharField(_("title"), max_length=10, choices=pro_title, default="Dr")
    professional_card = models.FileField(_("professional_card"), upload_to="professional_cards/%Y/%m/%D/", null=True, blank=True)
    diploma = models.FileField(_("diploma"), upload_to="diplomas/%Y/%m/%D/", null=True, blank=True)
    presentation = models.TextField(_("presentation"), null=True, blank=True)

    class Meta:
        """
        the place to configure de class or entities
        """
        verbose_name = _("Staff")
        verbose_name_plural = _("Staffs")
        ordering = ("-created_at",)

class StaffPath(BaseModel):
    path_types = (("FORMATION", "FORMATION"), ("EXPERIENCE", "EXPERIENCE"))
    staff = models.ForeignKey(Staffs, on_delete=models.CASCADE, related_name="staff_paths")
    description = models.TextField(_("description"),)
    start_year = models.IntegerField(_("start_date"))
    end_year = models.IntegerField(_("end_date"), null=True, blank=True)
    path_type = models.CharField(_("path_type"), max_length=20, choices=path_types, default="FORMATION")
    class Meta:
        """
        the place to configure de class or entities
        """
        verbose_name = _("StaffPath")
        verbose_name_plural = _("StaffPaths")
        ordering = ("-created_at",)

class PaymentMethod(BaseModel):
    payment_types = (
        ("ORANGE_MONEY", "ORANGE_MONEY"),
        ("MTN_MOBILE_MONEY", "MTN_MOBILE_MONEY")
    )
    payment_type = models.CharField(_("payment_type"), max_length=20, choices=payment_types, default="ORANGE_MONEY")
    phone_number = models.CharField(_("phone_number"), max_length=20)
    staff = models.ForeignKey(Staffs, on_delete=models.CASCADE, related_name="payment_methods")

    class Meta:
        """
        the place to configure de class or entities
        """
        verbose_name = _("PaymentMethod")
        verbose_name_plural = _("PaymentMethods")
        ordering = ("-created_at",)

class Pricing(BaseModel):
    pricing_types = (
        ("CHILD", "CHILD"),
        ("ADULT", "ADULT"),
        ("NORMAL", "NORMAL"),
        ("DISABLED", "DISABLED"),
    )
    amount = models.FloatField(_("amount"), default=0.0)
    pricing_type = models.CharField(_("pricing_type"), max_length=10, choices=pricing_types, default="NORMAL")
    staff = models.ForeignKey(Staffs, on_delete=models.CASCADE, related_name="staff_pricing")

    class Meta:
        """
        the place to configure de class or entities
        """
        verbose_name = _("Pricing")
        verbose_name_plural = _("Pricings")
        ordering = ("-created_at",)

class TimeSlots(BaseModel):
    days_of_week = (
        ("MONDAY", "MONDAY"),
        ("TUESDAY", "TUESDAY"),
        ("WEDNESDAY", "WEDNESDAY"),
        ("THURSDAY", "THURSDAY"),
        ("FRIDAY", "FRIDAY"),
        ("SATURDAY", "SATURDAY"),
        ("SUNDAY", "SUNDAY"),
        ("HOLIDAYS", "HOLIDAYS")
        
    )
    start_time = models.DateTimeField(_("start_time"), null=True, blank=True)
    end_time = models.DateTimeField(_("end_time"), null=True, blank=True)
    open_time = models.TimeField(_("open_time"), null=True, blank=True)
    close_time = models.TimeField(_("close_time"), null=True, blank=True)
    day_of_week = models.CharField(_("day_of_week"), max_length=20, choices=days_of_week, null=True, blank=True)
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

