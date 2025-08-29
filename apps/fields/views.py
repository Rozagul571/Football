from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .filters import FieldFilter
from .models import Field
from .serializers import FieldSerializer
from apps.account.models import UserAddress, User
from apps.booking.models import Booking
from .utils import calculate_distance
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter


class FieldListView(generics.ListAPIView):
    serializer_class = FieldSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = FieldFilter

    @extend_schema(
        parameters=[
            OpenApiParameter(name='start_time', type=str, location='query', description='Start time YYYY-MM-DD HH:MM:SS'),
            OpenApiParameter(name='end_time', type=str, location='query', description='End time YYYY-MM-DD HH:MM:SS'),
        ],
        responses={200: FieldSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        queryset = Field.objects.all()

        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')
        if start_time and end_time:
            queryset = Field.objects.filter(is_active=True)
            queryset = self.filter_queryset(queryset)
        elif not start_time and not end_time:
            queryset = Field.objects.all()
        else:
            return Response({"error": "start_time va end_time to'liq kiriting"}, status=400)


        last_address = UserAddress.objects.filter(user=request.user).first()
        if not last_address or not last_address.location:
            return Response({"error": "Manzil topilmadi"}, status=400)

        user_location = last_address.location
        if queryset.exists():
            queryset = sorted(queryset, key=lambda f: calculate_distance(user_location, f.address) or float('inf'))
        serializer = self.get_serializer(queryset, many=True, context={'user_location': user_location})
        return Response(serializer.data)

class FieldDetailView(generics.RetrieveAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: FieldSerializer})
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['Band qilingan maydon vaqtlar'] = list(Booking.objects.filter(field=instance, is_active=True).values('start_time', 'end_time'))
        return Response(data)

class FieldCreateView(generics.CreateAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        queryset = User.objects.filter()
        instance = serializer.save()
        return Response(serializer.data)


    @extend_schema(
        request=FieldSerializer,
        responses={201: FieldSerializer}
    )
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class FieldUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=FieldSerializer,
        responses={200: FieldSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

# class FieldAllView(generics.ListAPIView):
#     serializer_class = FieldSerializer
#     permission_classes = [IsAuthenticated]
#
#     @extend_schema(responses={200: FieldSerializer(many=True)})
#     def get(self, request, *args, **kwargs):
#         queryset = Field.objects.all()
#         serializer = self.get_serializer(queryset, many=True)
#         last_address = UserAddress.objects.filter(user=request.user).first()
#
#         if not last_address or not last_address.location:
#             return Response({"error": "Manzil topilmadi"}, status=400)
#
#         user_location = last_address.location
#         if queryset.exists():
#             queryset = sorted(queryset, key=lambda f: calculate_distance(user_location, f.address) or float('inf'))
#         serializer = self.get_serializer(queryset, many=True, context={'user_location': user_location})
#         return Response(serializer.data)
