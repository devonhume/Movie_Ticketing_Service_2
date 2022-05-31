from .ticket_handler import TicketHandler
from .models import Showing, Ticket
from .mail_handler import MailHandler

class BillingHandler:

    def __init__(self):
        self.status = True
        self.ticketer = TicketHandler()

    def ticket_total(self, tickets, showing_id):
        showing = Showing.objects.get(id=showing_id)
        if showing.seats_available < tickets:
            return False
        return showing.ticket_price * tickets

    def buy_tickets(self, purchases, billing_info):
        showing = Showing.objects.get(id=purchases['showing_id'])
        if showing.seats_available < purchases['adult_tickets'] + purchases['child_tickets']:
            return False

        tickets = self.ticketer.generate_tickets(
            showing_id=purchases['showing_id'],
            adult_tickets=purchases['adult_tickets'],
            child_tickets=purchases['child_tickets'],
            buyer=billing_info['buyer']
        )

        if tickets:
            if self.charge_customer(total=purchases['total'], billing_info=billing_info):
                mh = MailHandler()
                mh.send_tickets({'ticket_ids': tickets, 'showing_id': purchases['showing_id'], 'buyer': billing_info['buyer']})
                return True
            else:
                for ticket in tickets:
                    del_ticket = Ticket.objects.get(id=ticket)
                    del_ticket.delete()
                return False

    def charge_customer(self, total, billing_info):

        # Charge Customer via Electronic Billing API
        # If Successful, return True
        # If Charge Fails Return False

        print(f"Charging {billing_info['first_name']} {billing_info['last_name']} ${total} to credit card number "
              f"{billing_info['cc_number']}, exp date {billing_info['cc_month']}/{billing_info['cc_year']}, "
              f"code {billing_info['code']}")

        return True