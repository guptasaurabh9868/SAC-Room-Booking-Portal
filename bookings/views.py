import httplib2
import os
import datetime

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

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from decouple import config

# For google calendar
# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API (SAC Room Booking)'

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
        start = serializer.validated_data['start']
        end = serializer.validated_data['end']

        if start > end:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        bookings = Booking.objects.filter(room_id=serializer.validated_data['room_id'])
        
        for booking in bookings:
            curr_start = booking.start
            curr_end = booking.end

            if (curr_start <= start and start <= curr_end):
                return Response(BookingSerializer(booking).data, status=status.HTTP_406_NOT_ACCEPTABLE)

            if (curr_start <= end and end <= curr_end):
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

    start = booking.start
    end = booking.end
    
    for _booking in Booking.objects.filter(room_id=booking.room_id, approved=True, rejected=False):
        curr_start = _booking.start
        curr_end = _booking.end

        if booking.id == _booking.id:
            continue

        # check if bookings overlap
        if start <= curr_end and curr_start <= end:
            return _booking
    
    return False

def get_google_calendar_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)

    credential_path = os.path.join(credential_dir,
                                   'sac-room-booking-calendar.json')

    store = Storage(credential_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        flags = tools.argparser.parse_args(args=[])
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)

    return credentials

def get_google_calendar_service():
    credentials = get_google_calendar_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    return service

def create_calendar_event(booking):
    service = get_google_calendar_service()

    event = {
        'summary': booking.account.name,
        'location': str(booking.room_id),
        'description': '',
        'start': {
            'dateTime': booking.start.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': booking.end.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'attendees': [
            {'email': booking.account.email},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
            ],
        }
    }

    event = service.events().insert(
        calendarId=config('CALENDAR_ID'),
        body=event).execute()

    booking.googleCalendarEventId = event['id']
    return event

def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(data=request.POST)
        if form.is_valid():
            booking = form.save(commit=False)

            # TODO: Check if booking date/time is not before current date/time

            if booking.start > booking.end:
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
    create_calendar_event(booking)
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
