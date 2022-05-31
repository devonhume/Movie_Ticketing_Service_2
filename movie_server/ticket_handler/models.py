from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=250)
    image = models.URLField()
    runtime_hrs = models.IntegerField()
    runtime_mins = models.IntegerField()
    rating = models.CharField(max_length=250)


class Showing(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    ticket_price = models.DecimalField(decimal_places=2, max_digits=100)
    seats_available = models.IntegerField()
    seats_total = models.IntegerField()


class Ticket(models.Model):
    showing = models.ForeignKey(Showing, on_delete=models.CASCADE)
    ticket_code = models.CharField(max_length=50)
    ticket_type = models.CharField(max_length=50)
    ticket_used = models.BooleanField(default=False)
    buyer = models.EmailField()