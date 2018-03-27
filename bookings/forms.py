from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    booking_from = forms.CharField()
    booking_to = forms.CharField()

    class Meta:
        model = Booking
        fields = ('booking_from', 'booking_to', 'room_id')