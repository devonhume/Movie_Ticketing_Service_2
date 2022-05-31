import string
import random
from .models import Showing, Ticket


class TicketHandler:

    def __init__(self):
        self.status = True

    def generate_tickets(self, showing_id, adult_tickets, child_tickets, buyer):
        print("Generate Tickets")
        showing = Showing.objects.get(id=showing_id)
        ticket_ids = []
        if showing.seats_available < adult_tickets + child_tickets:
            return False
        elif adult_tickets or child_tickets:
            if adult_tickets:
                for i in range(adult_tickets):
                    new_code = self.generate_ticket_code()
                    new_ticket = Ticket(
                        showing=showing,
                        ticket_code=new_code,
                        ticket_type='adult',
                        ticket_used=False,
                        buyer=buyer
                    )
                    new_ticket.save()
                    ticket_ids.append(new_ticket.id)
            if child_tickets:
                for i in range(child_tickets):
                    new_code = self.generate_ticket_code()
                    new_ticket = Ticket(
                        showing=showing,
                        ticket_code=new_code,
                        ticket_type='child',
                        ticket_used=False,
                        buyer=buyer
                    )
                    new_ticket.save()
                    ticket_ids.append(new_ticket.id)
            return ticket_ids
        else:
            return False

    def generate_ticket_code(self):
        print("Generate Ticket Code")
        while True:
            code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
            try:
                Ticket.objects.get(ticket_code=code)
            except:
                return code

