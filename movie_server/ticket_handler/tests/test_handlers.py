from django.test import TestCase
from ..ticket_handler import TicketHandler
from ..billing_handler import BillingHandler
from ..mail_handler import MailHandler
from ..models import Showing, Ticket, Movie


# Tests for Billing_Handler:
# 1) Instantiate Billing handler class
# 2) Ticket_total
# 3) Buy_tickets
# 4) Charge Customer

class TestBillingHandler(TestCase):

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
        self.showing.seats_total = 10
        self.showing.movie = self.movie
        self.showing.save()

    # does BillingHandler successfully instantiate?
    def test_handler_create(self):
        handler = BillingHandler()
        self.assertEqual(handler.status, True)

    def test_buy_tickets(self):
        handler = BillingHandler()
        # showing = Showing.objects.get(id=1)

        # data for standard ticket order
        data_1_order = {
            'adult_tickets': 3,
            'child_tickets': 3,
            'showing_id': self.showing.id,
            'total': 3 * self.showing.ticket_price + 3 * self.showing.ticket_price / 2
        }
        data_1_billing_data = {
            'buyer': 'devonlearnscode@gmail.com',
            'first_name': 'test FN',
            'last_name': 'test_LN',
            'cc_number': 000000000000000,
            'cc_month': 00,
            'cc_year': 00,
            'code': 000
        }

        result = handler.buy_tickets(purchases=data_1_order, billing_info=data_1_billing_data)
        # did method return true
        self.assertEqual(result, False, msg='Able to buy 6 Tickets')

        # check tickets created

        # check number of adult tickets
        tickets = Ticket.objects.filter(showing=0, ticket_type='adult')
        count = 0
        for ticket in tickets:
            count += 1
        self.assertEqual(count, 3)

        # check number of child tickets
        tickets = Ticket.objects.filter(showing=0, ticket_type='child')
        count = 0
        for ticket in tickets:
            count += 1
        self.assertEqual(count, 3)

        # check total number of tickets found
        tickets = Ticket.objects.filter(showing=0)
        count = 0
        for ticket in tickets:
            count += 1
        self.assertEqual(count, 6)

        # check individual ticket attributes
        for ticket in tickets:
            self.assertNotEqual(ticket.ticket_code, None)
            self.assertEqual(ticket.ticket_used, 0)
            self.assertNotEqual(ticket.buyer, None)

        # cleanup test tickets
        for ticket in tickets:
            ticket.delete()

        # data for overselling
        data_2_order = {
            'adult_tickets': 8,
            'child_tickets': 3,
            'showing_id': 0,
            'total': 3 * self.showing.ticket_price + 3 * self.showing.ticket_price / 2
        }

        result = handler.buy_tickets(purchases=data_2_order, billing_info=data_1_billing_data)
        self.assertEqual(result, False)


# Tests for Ticket_handler
# 1) Instantiate Ticket Handler
# 2) get_all_movies
# 3) generate Tickets
# 4) generate ticket code

class TestTicketHandler(TestCase):

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


    def test_handler_create(self):
        handler = TicketHandler()
        self.assertEqual(handler.status, True)

    def test_generate_tickets(self):
        handler = TicketHandler()
        buyer = 'devonlearnscode@gmail.com'

        # test adult ticket creation
        result = handler.generate_tickets(self.showing.id, 5, 0, buyer)
        self.assertNotEqual(result, False)
        self.assertEqual(len(result), 5)

        for id in result:
            ticket = Ticket.objects.get(id=id)
            self.assertEqual(ticket.ticket_type, 'adult')
            self.assertEqual(ticket.ticket_used, 0)
            self.assertNotEqual(ticket.ticket_code, None)

        # cleanup test tickets
        for id in result:
            ticket = Ticket.objects.get(id=id)
            ticket.delete()

        # test child ticket creation
        result = handler.generate_tickets(self.showing.id, 0, 5, buyer)
        self.assertNotEqual(result, False)
        self.assertEqual(len(result), 5)

        for id in result:
            ticket = Ticket.objects.get(id=id)
            self.assertEqual(ticket.ticket_type, 'child')
            self.assertEqual(ticket.ticket_used, 0)
            self.assertNotEqual(ticket.ticket_code, None)

        # cleanup test tickets
        for id in result:
            ticket = Ticket.objects.get(id=id)
            ticket.delete()

        # Test overselling
        result = handler.generate_tickets(self.showing.id, 11, 0, buyer)
        self.assertEqual(result, False)

        # test no tickets passed
        result = handler.generate_tickets(self.showing.id, 0, 0, buyer)
        self.assertEqual(result, False)

# Tests for Mail Handler
# Send Tickets
# Build Tickets

# Tests for Server
# Home
# Showings
# Purchase
