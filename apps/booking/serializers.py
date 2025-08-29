from rest_framework import serializers
from .models import Booking
from apps.fields.serializers import FieldSerializer
from decimal import Decimal


class BookingSerializer(serializers.ModelSerializer):
    field_details = FieldSerializer(source='field', read_only=True)
    start_time = serializers.DateTimeField(input_formats=['%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%d %H:%M:%S'], required=True)
    end_time = serializers.DateTimeField(input_formats=['%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%d %H:%M:%S'], required=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'field', 'field_details', 'start_time', 'end_time', 'total_price', 'is_active']
        read_only_fields = ['id', 'user', 'is_active', 'total_price', 'field_details']

    def validate(self, data):
        field = data.get('field')
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if start_time >= end_time:
            raise serializers.ValidationError("Boshlanish vaqti tugash vaqtidan oldin (katta bo'lishi kerak")

        # if field and not field.is_active:
        #     raise serializers.ValidationError("Faol boʻlmagan maydonni band qilib boʻlmaydi")

        if Booking.objects.filter(field=field, is_active=True).filter(
                start_time__lt=end_time, end_time__gt=start_time
        ).exists():
            raise serializers.ValidationError("Bu vaqt oralig'i band qilingan")

        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        time_diff = Decimal(str((validated_data['end_time'] - validated_data['start_time']).total_seconds() / 3600))
        validated_data['total_price'] = validated_data['field'].price * time_diff
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        field_details = representation.pop('field_details')
        filtered_field_details = {
            'name': field_details['name'],
            'contact': field_details['contact'],
            'price': field_details['price'],
            'latitude': field_details['latitude'],
            'longitude': field_details['longitude']
        }
        representation['field_details'] = filtered_field_details

        representation.pop('id', None)
        representation.pop('user', None)
        representation.pop('field', None)
        representation.pop('is_active', None)
        # representation.pop('total_price', None)
        return representation