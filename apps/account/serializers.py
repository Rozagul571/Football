from phonenumber_field.phonenumber import PhoneNumber
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from apps.account.models import User, UserAddress
from django.contrib.gis.geos import Point


class RegisterSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "phone_number", "password")
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.phone_number:
            data['phone_number'] = str(instance.phone_number)
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'user'))
        return user

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already register")
        return value

class UserAddressSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)

    class Meta:
        model = UserAddress
        fields = ('id', 'latitude', 'longitude', 'user', 'location')
        read_only_fields = ('id', 'user', 'location')

    def create(self, validated_data):
        lat = validated_data.pop('latitude')
        lon = validated_data.pop('longitude')
        validated_data['location'] = Point(lon, lat)
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['latitude'] = instance.location.y if instance.location else None
        rep['longitude'] = instance.location.x if instance.location else None
        return rep



