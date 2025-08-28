from django.contrib import admin
from .models import Field


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "price", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "contact")
