import json
from django.shortcuts import render
from .models import *
from .utils import get_plot
from django.contrib.auth.decorators import login_required

# Auth example
# @login_required
# def protectd_view(request):
#   pass

# Create your views here.
def home(request):
    qs = Invoice_Line_Item.objects.all()
    x = [x.item.item_name for x in qs]
    y = [y.item_total for y in qs]
    chart = get_plot(x, y)
    return render(
        request,
        "home.html",
        {
            "chart": chart,
            "chartdatajson": json.dumps([12, 11, 19, 5, 2, 3]),
        },
    )


def customers(request):
    customers = Customer.objects.all()
    return render(
        request,
        "customers.html",
        {
            "customers": customers,
        },
    )


# This would be accessed with
# /fake-customer/?q=frank
def fake_customer_search(request):
    q = request.GET.get("q", None)
    qs = Customer.objects.all()

    if q is not None:
        customers = qs.filter(customer_name__icontains=q)

    return render(
        request,
        "customers.html",
        {
            "customers": customers,
        },
    )
