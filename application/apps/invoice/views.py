from django.contrib.auth.models import User
from application.apps.accounts.models import BusinessProfile
from application.apps.deals.models import Deal
from application.apps.invoice.models import Invoice
from django.shortcuts import render, get_object_or_404


def index(request, identifier):
    invoice = get_object_or_404(Invoice, identifier=identifier)

    return render(request, 'invoice/invoice.html', {"invoice": invoice})
