from bookings.models import Booking
from bookings.serializers import BookingSerilizer, UserSerializer
from rest_framework import generics
from django.http import Http404
from django.shortcuts import get_object_or_404
from rooms.models import Room
from django.contrib.auth.models import User
from rest_framework import permissions
from bookings.permissions import IsOwnerOrReadOnly

class BookingList(generics.ListCreateAPIView):
    """
    List all bookings, or create a new booking
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerilizer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        print(self.request.user)
        print(serializer.data)

class BookingDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a room
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerilizer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, 
        IsOwnerOrReadOnly,)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer