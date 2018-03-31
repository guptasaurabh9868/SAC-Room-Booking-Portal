from rest_framework import serializers
from bookings.models import Booking
from rooms.models import Room

class BookingSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='account.username')
    title = serializers.SerializerMethodField('set_title')

    def set_title(self, booking):
        return str(booking.room_id) + ' - ' + booking.account.name

    class Meta:
        model = Booking
        fields = ('id', 'start', 'end', 'room_id', 'username', 'title')