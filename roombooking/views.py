from django.shortcuts import render
from bookings.models import Booking
from authentication.views import account_login

def home(request):
    bookings = Booking.objects.all()
    return render(request, 'roombooking/home.html', {'bookings': bookings})