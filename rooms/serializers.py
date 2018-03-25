from rest_framework import serializers
from rooms.models import Room
from bookings.models import Booking
from bookings.serializers import BookingSerilizer

class RoomSerializer(serializers.ModelSerializer):
    # TODO: remove read_only
    bookings = BookingSerilizer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ('id', 'number', 'name', 'bookings')
    
    def create(self, validated_data):
        bookings_data = validated_data.pop('bookings', [])
        room = Room.objects.create(**validated_data)

        for booking_data in bookings_data:
            Booking.objects.create(room=room, **booking_data)

        return room