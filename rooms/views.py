from rooms.models import Room
from rooms.serializers import RoomSerializer
from rest_framework import generics
from django.http import Http404

class RoomList(generics.ListCreateAPIView):
    """
    List all rooms, or create a new room if POST request.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a room
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'number'

