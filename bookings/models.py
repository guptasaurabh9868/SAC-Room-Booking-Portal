from django.db import models
from rooms.models import Room

class Booking(models.Model):
    booking_from = models.DateTimeField()
    booking_to = models.DateTimeField()
    room_id = models.ForeignKey('rooms.Room', related_name='bookings', on_delete=models.CASCADE)
    account = models.ForeignKey('authentication.Account', related_name='bookings', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['booking_from']

    # def save(self, *args, **kwargs):
    #     super(Booking, self).save(*args, **kwargs)

    def __str__(self):
        return ' '.join([self.room, self.booking_from, self.booking_to])