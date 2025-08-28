from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db.models import PointField
from django.core.exceptions import ValidationError
from django.db import models
from apps.account.managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    phone_number = PhoneNumberField(unique=True, null=False, blank=False)
    class Role(models.TextChoices):
        OWNER = 'owner', 'Owner'
        ADMIN = 'admin', 'Administrator'
        User = 'user', 'User'
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    username = None
    objects = UserManager()
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.User)

    def save(self, *args, **kwargs):
        if self.pk:
            orig = User.objects.get(pk=self.pk)
            if orig.phone_number != self.phone_number:
                raise ValidationError("Phone number cannot be changed")
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.phone_number)


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address = models.CharField(max_length=255)
    location = PointField(srid=4326)

    def __str__(self):
        return str(self.address)

