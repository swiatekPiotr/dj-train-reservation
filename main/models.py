from django.db import models
from django.utils import timezone


class Course(models.Model):
    start = models.CharField(max_length=120)
    end = models.CharField(max_length=120)
    start_time = models.TimeField(default=timezone.now())
    end_time = models.TimeField()
    time = models.TimeField()

    def __str__(self):
        return f"from {self.start} to {self.end}"


class Station(models.Model):
    lp_station = models.PositiveIntegerField()
