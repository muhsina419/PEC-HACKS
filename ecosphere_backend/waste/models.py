from django.conf import settings
from django.db import models
from django.utils import timezone


class EcoCycleItem(models.Model):
    STATUS_RECYCLED = "recycled"
    STATUS_REUSED = "reused"
    STATUS_COMPOSTED = "composted"
    STATUS_LANDFILL = "landfill"
    STATUS_NONE = "none"

    DISPOSAL_STATUS_CHOICES = [
        (STATUS_RECYCLED, "Recycled"),
        (STATUS_REUSED, "Reused / Refilled"),
        (STATUS_COMPOSTED, "Composted"),
        (STATUS_LANDFILL, "Landfill"),
        (STATUS_NONE, "No update"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    packaging = models.CharField(max_length=255, blank=True)
    expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    disposal_status = models.CharField(
        max_length=20,
        choices=DISPOSAL_STATUS_CHOICES,
        default=STATUS_NONE,
    )
    disposal_proof_url = models.URLField(blank=True)
    disposal_notes = models.TextField(blank=True)
    disposal_logged_at = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

    def days_left(self):
        return (self.expiry_date - timezone.now().date()).days

    def calculate_score(self) -> int:
        proof = bool(self.disposal_proof_url)
        if self.disposal_status == self.STATUS_RECYCLED:
            return 10 if proof else 3
        if self.disposal_status == self.STATUS_REUSED:
            return 8
        if self.disposal_status == self.STATUS_COMPOSTED:
            return 6
        if self.disposal_status == self.STATUS_LANDFILL:
            return 0

        days_after_expiry = (timezone.now().date() - self.expiry_date).days
        if days_after_expiry > 1:
            return -10
        if days_after_expiry >= 0:
            return -5
        return 0

    def save(self, *args, **kwargs):
        # Keep score in sync whenever disposal_status or proof changes.
        self.score = self.calculate_score()
        super().save(*args, **kwargs)
