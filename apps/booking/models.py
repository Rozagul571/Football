from django.db import models
from apps.account.models import User
from apps.fields.models import Field

class Booking(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("field", "start_time", "end_time")

    def __str__(self):
        return f"{self.field.name} - {self.user.phone_number} - {self.start_time}"



