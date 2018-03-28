from bookings.models import Booking
from bookings.serializers import BookingSerializer
from rooms.models import Room
from rest_framework import permissions
from bookings.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework import status
import dateutil.parser
import pytz

from django.shortcuts import render, HttpResponseRedirect
from .forms import BookingForm
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

class BookingViewSet(viewsets.ModelViewSet):
    """
    List all bookings, create, retrieve, update
    and destroy a booking
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(account=self.request.user)

    # def get_parsed_date(self, date):
    #     return dateutil.parser.parse(date)

    def check_date_range_conflict(self, request, serializer):
        booking_from = serializer.validated_data['booking_from']
        booking_to = serializer.validated_data['booking_to']

        if booking_from > booking_to:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        bookings = Booking.objects.filter(room_id=serializer.validated_data['room_id'])
        
        for booking in bookings:
            curr_booking_from = booking.booking_from
            curr_booking_to = booking.booking_to

            if (curr_booking_from <= booking_from and booking_from <= curr_booking_to):
                return Response(BookingSerializer(booking).data, status=status.HTTP_406_NOT_ACCEPTABLE)

            if (curr_booking_from <= booking_to and booking_to <= curr_booking_to):
                return Response(BookingSerializer(booking).data, status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer.save(account=request.user)
        return Response(serializer.data)

    def create(self, request, pk=None, format=None):
        serializer = BookingSerializer(data=request.data)
        print(request.data)

        if serializer.is_valid():
            return self.check_date_range_conflict(request, serializer)

    # TODO: Implement method to update booking dates

def get_conflicted_booking_or_false(booking):

    booking_from = booking.booking_from
    booking_to = booking.booking_to
    
    for _booking in Booking.objects.filter(room_id=booking.room_id, approved=True, rejected=False):
        curr_booking_from = _booking.booking_from
        curr_booking_to = _booking.booking_to

        if booking.id == _booking.id:
            continue
            
        # check if bookings overlap
        if booking_from <= curr_booking_to and curr_booking_from <= booking_to:
            return _booking
    
    return False

def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(data=request.POST)
        if form.is_valid():
            booking = form.save(commit=False)

            # TODO: Check if booking date/time is not before current date/time

            if booking.booking_from > booking.booking_to:
                return render(request, 'bookings/create_booking.html', {'form': form, 'msg': 'Invalid date range'})

            # _booking will be Booking object if there is a conflict
            # or False otherwise
            _booking = get_conflicted_booking_or_false(booking)

            if _booking != False:
                return render(request, 'bookings/create_booking.html', {'form': form, 'booking': [_booking], 'msg': 'Conflicts with following booking:'})
            
            booking.account=request.user
            booking.save()
            
            return HttpResponseRedirect('/bookings')
        else:
            return render(render(request, 'bookings/create_booking.html', {'form': form, 'msg': 'Form not valid!'}))        
    else:
        form = BookingForm()

    return render(request, 'bookings/create_booking.html', {'form': form})

def show_bookings(request):
    if request.user.is_admin:
        bookings = Booking.objects.filter()
    else:
        bookings = Booking.objects.filter(account=request.user)
    return render(request, 'bookings/show_bookings.html', {'bookings': bookings})

def send_email(request, status, booking):
    if not request.user.is_admin:
        return
    subject = "SAC Room Booking status"

    message = render_to_string('bookings/booking_email.html', {
        'account': booking.account,
        'booking': booking,
        'status': status
    })

    to_email = booking.account.email
    email = EmailMessage(
        subject, message, to=[to_email]
    )

    email.send()

def delete_booking(request, pk):
    booking = Booking.objects.get(id=pk)
    send_email(request, "deleted", booking)
    booking.delete()
    return HttpResponseRedirect('/bookings/')

def approve_booking(request, pk):
    booking = Booking.objects.get(id=pk)

    _booking = get_conflicted_booking_or_false(booking)

    if _booking != False:
        return HttpResponseRedirect('/bookings/conflict?id1=' + str(booking.id) + '&id2=' + str(_booking.id))

    booking.approved = True
    booking.rejected = False
    booking.save()
    send_email(request, "approved", booking)  
 
    return HttpResponseRedirect('/bookings/')

def booking_conflict(request):
    booking1 = Booking.objects.get(id=request.GET.get('id1'))
    booking2 = Booking.objects.get(id=request.GET.get('id2'))

    return render(request, 'bookings/booking_conflict.html', {'bookings': [booking1, booking2]})

def reject_booking(request, pk):
    booking = Booking.objects.get(id=pk)
    booking.rejected = True
    booking.approved = False
    booking.save()
    send_email(request, "rejected", booking)    
    return HttpResponseRedirect('/bookings/')
