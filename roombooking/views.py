from django.shortcuts import render
from bookings.models import Booking

def home(request):
    bookings = Booking.objects.all()
    return render(request, 'roombooking/home.html', {'bookings': bookings})