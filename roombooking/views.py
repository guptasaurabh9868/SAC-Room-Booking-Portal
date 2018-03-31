from django.shortcuts import render
from django.db.models import Q
from bookings.models import Booking
from authentication.views import account_login

def home(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            bookings = Booking.objects.filter(~Q(status=1))
        else:
            bookings = Booking.objects.filter(~Q(status=1), account=request.user)
    else:        
        bookings = []
    return render(request, 'roombooking/home.html', {'total_bookings': len(bookings)})