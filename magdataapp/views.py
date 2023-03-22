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

    # CHARTJS CHART
    categories = ["Disposable vapes", "Cloud 8", "Vape Juice", "Rolling Tobacco"]
    aggregations = []
    for category in categories:
        qs = Invoice_Line_Item.objects.filter(item__category_name = category) 
        total = 0
        for line_item in qs:
            total += line_item.item_total
        aggregations.append(total)

    
    
    return render(
        request,
        "home.html",
        {
            "chart": chart,
            "chartdatajson": json.dumps(aggregations),
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
