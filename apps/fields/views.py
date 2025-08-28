from django.utils.dateparse import parse_datetime
from rest_framework import generics
from django.contrib.gis.db.models.functions import Distance
from rest_framework.permissions import IsAuthenticated
from .models import Field
from .serializers import FieldSerializer
from apps.account.permissions import IsOwnerOrAdmin
from django.contrib.gis.geos import Point
from apps.booking.models import Booking


class FieldCreateView(generics.CreateAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    # parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FieldListView(generics.ListAPIView):
    queryset = Field.objects.filter(is_active=True)
    serializer_class = FieldSerializer
    permission_classes = [IsAuthenticated]


class FieldDetailView(generics.RetrieveAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    permission_classes = [IsAuthenticated]


class FieldUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

class AvailableFieldListView(generics.ListAPIView):
    serializer_class = FieldSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Field.objects.filter(is_active=True)

        start_time = self.request.query_params.get("start_time")
        end_time = self.request.query_params.get("end_time")
        lat = self.request.query_params.get("latitude")
        lon = self.request.query_params.get("longitude")

        if start_time and end_time:
            start = parse_datetime(start_time)
            end = parse_datetime(end_time)
            booked_fields = Booking.objects.filter(
                start_time__lt=end,
                end_time__gt=start,
                is_active=True
            ).values_list("field_id", flat=True)
            queryset = queryset.exclude(id__in=booked_fields)


        if lat and lon:
            user_location = Point(float(lon), float(lat), srid=4326)
            queryset = queryset.annotate(
                distance=Distance("address", user_location)).order_by("distance")
        return queryset
