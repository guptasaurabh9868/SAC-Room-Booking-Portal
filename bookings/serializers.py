from rest_framework import serializers
from bookings.models import Booking
from rooms.models import Room

class BookingSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='account.username')

    class Meta:
        model = Booking
        fields = ('id', 'booking_from', 'booking_to', 'room_id', 'username')