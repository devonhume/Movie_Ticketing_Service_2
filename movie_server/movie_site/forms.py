from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TicketsForm(forms.Form):
    adult_tickets = forms.IntegerField(label="Adult Tickets (13 and up)")
    child_tickets = forms.IntegerField(label="Child Tickets (12 and under)")


class PurchaseForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    email = forms.EmailField(label="Email")
    credit_card = forms.IntegerField(label="Credit Card")
    exp_month = forms.IntegerField(label="Expiration Month")
    exp_year = forms.IntegerField(label="Expiration Year")
    secret_code = forms.IntegerField(label="Secret Code")


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


