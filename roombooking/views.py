from django.shortcuts import render
from django.db.models import Q
from bookings.models import Booking
from authentication.views import account_login

def home(request):
    bookings = Booking.objects.filter(~Q(status=1), account=request.user)
    return render(request, 'roombooking/home.html', {'total_bookings': len(bookings)})