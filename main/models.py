from django.db import models
from django.utils import timezone


class Course(models.Model):
    start = models.CharField(max_length=120)
    end = models.CharField(max_length=120)
    start_time = models.TimeField(default=timezone.now())
    end_time = models.TimeField()
    time = models.TimeField()

    def __str__(self):
        return f"from {self.start} -> to {self.end}"


class Station(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Timetable(models.Model):
    courses = models.ForeignKey(Course, on_delete=models.CASCADE)
    stations = models.ForeignKey(Station, on_delete=models.CASCADE)
    lp_station = models.PositiveIntegerField()
    at_location = models.TimeField(default=timezone.now())


class Carriage(models.Model):
    courses = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"car number:{self.id} ({self.courses})"


class Seating(models.Model):
    carriages = models.ForeignKey(Carriage, on_delete=models.CASCADE)

    def __str__(self):
        return f"seat number: {self.id} of carriage: {self.carriages}"
