from django.db import models

class Room(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=False)

    class Meta:
        ordering = ('number',)

    def __unicode__(self):
        return ' '.join([self.number, self.name])