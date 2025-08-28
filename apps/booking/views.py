from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import BookingSerializer


class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
