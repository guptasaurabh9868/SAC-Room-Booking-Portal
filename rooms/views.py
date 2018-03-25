from django.shortcuts import render
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rooms.models import Room
from rooms.serializers import RoomSerializer

class RoomList(APIView):
    """
    List all rooms, or create a new room if POST request.
    """
    def get(self, request, format=None):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RoomSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomDetail(APIView):
    """
    Retrieve, update or delete a room
    """
    def get_object(self, number):
        try:
            room = Room.objects.get(number=number)
            return room
        except Room.DoesNotExist:
            raise Http404

    def get(self, request, number, format=None):
        room = self.get_object(number)
        serializer = RoomSerializer(room)
        return Response(serializer.data)

    def put(self, request, number, format=None):
        room = self.get_object(number)
        serializer = RoomSerializer(room, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, number, format=None):
        room = self.get_object(number)
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

