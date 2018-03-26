from bookings.models import Booking
from bookings.serializers import BookingSerializer, UserSerializer
from rooms.models import Room
from django.contrib.auth.models import User
from rest_framework import permissions
from bookings.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework import status
import dateutil.parser

class BookingViewSet(viewsets.ModelViewSet):
    """
    List all bookings, create, retrieve, update
    and destroy a booking
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def get_parsed_date(self, date):
    #     return dateutil.parser.parse(date)

    def check_date_range_conflict(self, request, serializer):
        booking_from = serializer.validated_data['booking_from']
        booking_to = serializer.validated_data['booking_to']

        bookings = Booking.objects.filter(room_id=serializer.validated_data['room_id'])
        
        for booking in bookings:
            curr_booking_from = booking.booking_from
            curr_booking_to = booking.booking_to

            if (curr_booking_from <= booking_from and booking_from <= curr_booking_to):
                return Response(BookingSerializer(booking).data, status=status.HTTP_406_NOT_ACCEPTABLE)

            if (curr_booking_from <= booking_to and booking_to <= curr_booking_to):
                return Response(BookingSerializer(booking).data, status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer.save(user=request.user)
        return Response(serializer.data)

    def create(self, request, pk=None, format=None):
        serializer = BookingSerializer(data=request.data)
        print(request.data)

        if serializer.is_valid():
            return self.check_date_range_conflict(request, serializer)

    # TODO: Implement method to update booking dates

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer