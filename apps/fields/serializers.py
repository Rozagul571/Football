from rest_framework import serializers
from django.contrib.gis.geos import Point
from .models import Field

class FieldSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)

    class Meta:
        model = Field
        fields = [
            "id", "owner", "name", "contact", "price", "is_active",
            "latitude", "longitude"
        ]
        read_only_fields = ("id", "owner", "is_active")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.address:
            data["latitude"] = instance.address.y
            data["longitude"] = instance.address.x
        return data

    def create(self, validated_data):
        lat = validated_data.pop("latitude")
        lng = validated_data.pop("longitude")

        validated_data["address"] = Point(lng, lat, srid=4326)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        lat = validated_data.pop("latitude", None)
        lng = validated_data.pop("longitude", None)
        if lat and lng:
            validated_data["address"] = Point(lng, lat, srid=4326)
        return super().update(instance, validated_data)


    # def get_latitude(self, obj):
    #     return obj.address.y if obj.address else None
    #
    # def get_longitude(self, obj):
    #     return obj.address.x if obj.address else None


