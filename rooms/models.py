from django.db import models

class Room(models.Model):
    number = models.IntegerField(unique=True)
    name = models.CharField(max_length=100, blank=False)
    
    class Meta:
        ordering = ('number',)

    def __str__(self):
        return ' '.join([str(self.number), '-', self.name])