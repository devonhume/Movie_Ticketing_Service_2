from django.test import TestCase
from ..models import Movie, Showing, Ticket


class ModelsTest(TestCase):

	def setUp(self):
		self.movie = Movie()
		self.movie.title = "I am a title"
		self.movie.image = "http://i-am-a-test-image.com"
		self.movie.runtime_hrs = 2
		self.movie.runtime_mins = 30
		self.movie.rating = "None"
		self.movie.save()

		self.showing = Showing()
		self.showing.date = "2022-05-17"
		self.showing.time = "06:00"
		self.showing.ticket_price = 10.00
		self.showing.seats_available = 10
		self.showing.seats_total = 20
		self.showing.movie = self.movie
		self.showing.save()

		self.ticket = Ticket()
		self.ticket.ticket_code = "0000000000"
		self.ticket.ticket_type = "adult"
		self.ticket.ticket_used = False
		self.ticket.buyer = "test@test.com"
		self.ticket.showing = self.showing
		self.ticket.save()

	def test_movie_fields(self):
		record = Movie.objects.get(pk=self.movie.id)
		self.assertEqual(record, self.movie)

	def test_showing_fields(self):
		record = Showing.objects.get(pk=self.showing.id)
		self.assertEqual(record, self.showing)

	def test_ticket_fields(self):
		record = Ticket.objects.get(pk=self.ticket.id)
		self.assertEqual(record, self.ticket)

