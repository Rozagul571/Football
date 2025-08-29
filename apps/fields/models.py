from django.db import models
from django.contrib.gis.db.models import PointField
from phonenumber_field.modelfields import PhoneNumberField
from config import settings


class Field(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="fields")
    name = models.CharField(max_length=100)
    address = PointField(geography=True, srid=4326, null=True, blank=True)
    contact = PhoneNumberField(unique=True, null=False, blank=False)
    # image = models.ImageField(upload_to="fields/", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

