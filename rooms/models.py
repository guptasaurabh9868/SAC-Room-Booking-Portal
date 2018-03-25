from django.db import models

class Room(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=100, blank=False)

    class Meta:
        ordering = ('number',)