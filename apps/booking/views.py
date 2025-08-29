from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer
from .filters import BookingFilter
from apps.fields.models import Field

class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all().distinct()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookingFilter

    @extend_schema(
        request=BookingSerializer,
        responses={201: BookingSerializer}
    )
    def post(self, request, *args, **kwargs):
        field_id = request.data.get('field')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')

        if not field_id or not start_time or not end_time:
            return Response({"error": "Maydon boshlanish vaqti va tugash vaqti toliq kirirtilishi kerak"}, status=400)

        try:
            field = Field.objects.get(id=field_id)
        except Field.DoesNotExist:
            return Response({"error": "Maydon mavjud emas"}, status=400)

        data = {
            'field': field_id,
            'start_time': start_time,
            'end_time': end_time
        }
        serializer = self.get_serializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(serializer.data, status=201)

class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: BookingSerializer(many=True)})
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user, is_active=True)

class BookingDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: BookingSerializer})
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user, is_active=True)