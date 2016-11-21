from __future__ import unicode_literals
from ..login.models import User
from django.db import models
import datetime

# Create your models here.
class TripManager(models.Manager):
    def add_trip(self, data):
        now = datetime.datetime.now()
        errors = []

        if not data['destination']:
            errors.append('Destination field may not remain blank.')
        if not data['start_date']:
            errors.append('Travel Date From field may not remain blank.')
        elif data['start_date'] < str(now):
            errors.append('Trip may not start in the past')
        if not data['end_date']:
            errors.append('Travel Date to field may not remain blank.')
        elif data['start_date'] > data['end_date']:
            errors.append('Trip may not end before it starts')
        if not data['description']:
            errors.append('Description field may not remain blank.')

        return errors

class Trip(models.Model):
    destination = models.CharField(max_length=350)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    trip_creator = models.ForeignKey(User, related_name = 'trips')
    joiner = models.ManyToManyField(User, related_name = 'travel_buddy')

    objects = TripManager()
