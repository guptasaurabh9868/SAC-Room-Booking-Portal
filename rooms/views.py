from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rooms.models import Room
from rooms.serializers import RoomSerializer

@csrf_exempt
def room_list(request):
    """
    List all rooms, or create a new room if POST request.
    """
    if request.method == 'GET':
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RoomSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def room_detail(request, number):
    """
    Retrieve, update or delete a room
    """
    try:
        room = Room.objects.get(number=number)
    except Room.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = RoomSerializer(room)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = RoomSerializer(room, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        room.delete()
        return HttpResponse(status=204)

