from bookings.models import Booking
from bookings.serializers import BookingSerilizer
from rest_framework import generics
from django.http import Http404
from rooms.models import Room

class BookingList(generics.ListCreateAPIView):
    """
    List all bookings, or create a new booking
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerilizer

    # def perform_create(self, serializer):
    #     print(self.request.data)
    #     room = Room.objects.get(pk=self.request.data['room'])
    #     serializer.save(room=room)

class BookingDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a room
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerilizer
    # lookup_field = 'number'