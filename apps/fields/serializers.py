from rest_framework import serializers
from django.contrib.gis.geos import Point
from .models import Field
from .utils import calculate_distance

class FieldSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True, required=False)
    longitude = serializers.FloatField(write_only=True, required=False)
    distance = serializers.SerializerMethodField()

    class Meta:
        model = Field
        fields = ['id', 'owner', 'name', 'contact', 'price', 'is_active', 'latitude', 'longitude', 'distance']
        read_only_fields = ['id', 'owner', 'is_active', 'distance']


    def get_distance(self, obj):
        user_location = self.context.get('user_location')
        return calculate_distance(user_location, obj.address) if user_location and obj.address else None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.address:
            data['latitude'] = instance.address.y
            data['longitude'] = instance.address.x
        return data

    def create(self, validated_data):
        lat = validated_data.pop('latitude', None)
        lng = validated_data.pop('longitude', None)
        if lat and lng:
            validated_data['address'] = Point(lng, lat, srid=4326)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        lat = validated_data.pop('latitude', None)
        lng = validated_data.pop('longitude', None)
        if lat and lng:
            validated_data['address'] = Point(lng, lat, srid=4326)
        return super().update(instance, validated_data)