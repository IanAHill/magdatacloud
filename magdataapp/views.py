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

    # Pseudocode 
    # categories = ["Cat1", "Cat2", "Cat3", "Cat4", "Cat5"]
    # aggregations = []
    # for category in categories:
    #     qs = Invoice_Line_Items.objects.filter(category=category)
    #     total = 0
    #     for line_item in qs:
    #         total += line_item.item_total
    #     aggregations.append(total) 
    #
    # chartdatajson = json.dumps(aggregations)
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
