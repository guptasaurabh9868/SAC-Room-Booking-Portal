from rooms.models import Room
from rooms.serializers import RoomSerializer
from rest_framework import generics
from django.http import Http404
from rest_framework import permissions
from rest_framework import viewsets

class RoomViewSet(viewsets.ModelViewSet):
    """
    List all bookings, create, retrieve, update
    and destroy a room
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'number'
    
