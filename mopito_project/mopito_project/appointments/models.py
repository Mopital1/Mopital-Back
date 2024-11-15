from django.db import models
from django.utils.translation import gettext_lazy as _

from mopito_project.core.models import BaseModel
from mopito_project.actors.models import Patients, Staffs

class Appointment(BaseModel):
    """Model definition for Appointment."""
    # appointment status
    appointment_status = (
        ("PENDING", "PENDING"),
        ("CONFIRMED", "CONFIRMED"),
        ("CANCELLED", "CANCELLED"),
        ("COMPLETED", "COMPLETED"),
    )
    appointment_date = models.DateTimeField(_("appointment_date"), null=True, blank=True)
    description = models.TextField(_("description"), null=True, blank=True)
    # appointment_time = models.TimeField(_("appointment_time"))
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, related_name="appointments")
    staff = models.ForeignKey(Staffs, on_delete=models.CASCADE, related_name="appointments")
    status = models.CharField(_("status"), max_length=10, choices=appointment_status, default="PENDING")

    class Meta:
        """Meta definition for Appointment."""
        verbose_name = _("Appointment")
        verbose_name_plural = _("Appointments")
        ordering = ("created_at",)

    # def __str__(self):
    #     """Unicode representation of Appointment."""
    #     return f"{self.patient} - {self.doctor}"

    # def get_absolute_url(self):
    #     return reverse("Appointment_detail", kwargs={"pk": self.pk})

class Review(BaseModel):
    """Model definition for Review."""
    rating = models.FloatField(_("rating"))
    comment = models.TextField(_("comment"))
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="review")
    review_date = models.DateTimeField(_("review_date"), null=True, blank=True)

    class Meta:
        """Meta definition for Review."""
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")
        ordering = ("created_at",)

    # def __str__(self):
    #     """Unicode representation of Review."""
    #     return f"{self.rating} - {self.appointment}"
    # def get_absolute_url(self):
    #     return reverse("Review_detail", kwargs={"pk": self.pk})

class Consultation(BaseModel):
    """Model definition for Prescription."""
    consultation_date = models.DateTimeField(_("consultation_date"), null=True, blank=True)
    prescription = models.TextField(_("prescription"))
    result = models.TextField(_("result"))
    antecedent = models.TextField(_("antecedent"))
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="consultation")

    class Meta:
        """Meta definition for Prescription."""
        verbose_name = _("Prescription")
        verbose_name_plural = _("Prescriptions")
        ordering = ("created_at",)

    # def __str__(self):
    #     """Unicode representation of Prescription."""
    #     return f"{self.prescription_date} - {self.appointment}"
    # def get_absolute_url(self):
    #     return reverse("Prescription_detail", kwargs={"pk": self.pk})

class Notification(BaseModel):
    """Model definition for Notification."""
    # notification type
    notification_type = (
        ("PUSH", "PUSH"),
        ("SMS", "SMS"),
        ("EMAIL", "EMAIL"),
    )
    notification_date = models.DateTimeField(_("notification_date"), null=True, blank=True)
    content = models.TextField(_("content"), null=True, blank=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="notification")
    notification_type = models.CharField(_("notification_type"), max_length=10, choices=notification_type, default="PENDING")

    class Meta:
        """Meta definition for Notification."""
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        ordering = ("created_at",)

    # def __str__(self):
    #     """Unicode representation of Notification."""
    #     return f"{self.notification_date} - {self.appointment}"
    # def get_absolute_url(self):
    #     return reverse("Notification_detail", kwargs={"pk": self.pk})

# class Advertise(BaseModel):
#     """Model definition for Advertise."""
#     advertise_date = models.DateTimeField(_("advertise_date"), null=True, blank=True)
#     content = models.TextField(_("content"), null=True, blank=True)
    
#     class Meta:
#         """Meta definition for Advertise."""
#         verbose_name = _("Advertise")
#         verbose_name_plural = _("Advertises")
#         ordering = ("created_at",)

    # def __str__(self):
    #     """Unicode representation of Advertise."""
    #     return f"{self.advertise_date} - {self.appointment}"
    # def get_absolute_url(self):
    #     return reverse("Advertise_detail", kwargs={"pk": self.pk})