from django.shortcuts import render, redirect
from ticket_handler.models import Movie, Showing
from ticket_handler.ticket_handler import TicketHandler
from ticket_handler.billing_handler import BillingHandler
from .forms import TicketsForm, PurchaseForm, NewUserForm
from django.contrib.auth import login
from django.contrib import messages

# Create Handler Objects

ticketer = TicketHandler()
biller = BillingHandler()
adult_tickets = 0
child_tickets = 0
total_tickets = 0
purchase_flag = 0


# ----------- Routes --------------


# Home

def home_view(request, *args, **kwargs):
    current_movies = Movie.objects.all()
    context = {
        'movies': current_movies
    }
    return render(request, "index.html", context)


def showings_view(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    context = {
        'movie': movie
    }
    return render(request, "showings.html", context)


def purchase_view(request, showing_id):
    global adult_tickets
    print(f"Adult Tickets: {adult_tickets}")
    global child_tickets
    print(f"Child Tickets: {child_tickets}")
    global total_tickets
    print(f"Total Tickets: {total_tickets}")
    global purchase_flag
    print(f"Purchase Flag: {purchase_flag}")
    showing = Showing.objects.get(id=showing_id)
    movie = Movie.objects.get(id=showing.movie.id)
    ticket_form = TicketsForm()
    purchase_form = PurchaseForm()
    ticket_flag = False
    if total_tickets > showing.seats_available:
        ticket_flag = True
    if request.method == 'POST':
        ticket_form = TicketsForm(request.POST)
        purchase_form = PurchaseForm(request.POST)
        print(request.POST)
        print(request.POST.get("ticket_numbers"))
        print(f"ticket_form is valid: {ticket_form.is_valid()}")
        print(f"Ticket Errors: {ticket_form.errors}")
        print(f"purchase_form is valid: {purchase_form.is_valid()}")
        print(f"Purchase Errors: {purchase_form.errors}")
        if request.POST.get("ticket_numbers") == "ticket_numbers" and ticket_form.is_valid():
            print("Tickets Submitted")
            adult_tickets = ticket_form.cleaned_data['adult_tickets']
            child_tickets = ticket_form.cleaned_data['child_tickets']
            total_tickets = adult_tickets + child_tickets
            return redirect('purchase', showing_id)
        if request.POST.get("purchase_submit") == "purchase_tickets" and purchase_form.is_valid():
            print("Tickets Purchased")
            order = {
                'adult_tickets': adult_tickets,
                'child_tickets': child_tickets,
                'showing_id': showing_id,
                'total': adult_tickets * showing.ticket_price + child_tickets * showing.ticket_price / 2
            }
            print(order)
            billing_data = {
                'buyer': purchase_form.cleaned_data['email'],
                'first_name': purchase_form.cleaned_data['first_name'],
                'last_name': purchase_form.cleaned_data['last_name'],
                'cc_number': purchase_form.cleaned_data['credit_card'],
                'cc_month': purchase_form.cleaned_data['exp_month'],
                'cc_year': purchase_form.cleaned_data['exp_year'],
                'code': purchase_form.cleaned_data['secret_code']
            }
            print(billing_data)
            if biller.buy_tickets(purchases=order, billing_info=billing_data):
                new_seats = showing.seats_available - total_tickets
                showing.seats_available = new_seats
                showing.save()
                adult_tickets = 0
                child_tickets = 0
                total_tickets = 0
                purchase_flag = 1
                return redirect('purchase', showing_id)
            else:
                purchase_flag = 2
                return redirect('purchase', showing_id)
        if request.POST.get("success_submit") == "success_submit":
            purchase_flag = 0
            return redirect('home')
        if request.POST.get("fail_submit") == "fail_submit":
            purchase_flag = 0
            return redirect('purchase', showing_id)

    context = {
        'showing': showing,
        'movie': movie,
        'adult_price': showing.ticket_price,
        'child_price': showing.ticket_price / 2,
        'adult_tickets': adult_tickets,
        'child_tickets': child_tickets,
        'total_price': showing.ticket_price * adult_tickets + showing.ticket_price * child_tickets / 2,
        'ticket_form': ticket_form,
        'purchase_form': purchase_form,
        'ticket_flag': ticket_flag,
        'purchase_flag': purchase_flag
    }

    return render(request, "purchase.html", context)


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
        messages.error(request, "Unsuccessful registration. Invalid Information.")
    form = NewUserForm()
    return render (request=request, template_name='register.html', context={"register_form":form})


def jspractice(request):
    context = {}
    return render(request, "jspractice.html", context)


