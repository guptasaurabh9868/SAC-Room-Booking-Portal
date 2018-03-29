from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    start = forms.CharField()
    end = forms.CharField()

    class Meta:
        model = Booking
        fields = ('start', 'end', 'room_id')