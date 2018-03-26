from rest_framework import serializers
from bookings.models import Booking
from rooms.models import Room
from django.contrib.auth.models import User

class BookingSerilizer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Booking
        fields = ('id', 'booking_from', 'booking_to', 'room_id', 'user')

class UserSerializer(serializers.ModelSerializer):
    bookings = serializers.PrimaryKeyRelatedField(many=True, queryset=Booking.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'bookings')