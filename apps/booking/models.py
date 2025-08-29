from django.db import models
from apps.account.models import User
from apps.fields.models import Field

class Booking(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # distance = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ("field", "start_time", "end_time")

    def __str__(self):
        return f"{self.field.name} - {self.user.phone_number} - {self.start_time}"