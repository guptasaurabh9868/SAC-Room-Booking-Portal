from django.db import models
from rooms.models import Room

class Booking(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    room_id = models.ForeignKey('rooms.Room', related_name='bookings', on_delete=models.CASCADE)
    account = models.ForeignKey('authentication.Account', related_name='bookings', on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    googleCalendarEventId = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['start']

    # def save(self, *args, **kwargs):
    #     super(Booking, self).save(*args, **kwargs)

    def __str__(self):
        return ' '.join([str(self.room_id), str(self.start), str(self.end)])