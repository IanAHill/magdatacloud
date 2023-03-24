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
    categories = ["Disposable vapes", "THC8", "Vape Juice", "Rolling Tobacco"]
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

def items(request):
    items = Item.objects.all()
    return render(
        request,
        "items.html",
        {
            "items": items,
        },
    )

def invoices(request):
    invoices = Invoice_Line_Item.objects.all()
    return render(
        request,
        "invoices.html",
        {
            "invoices": invoices,
        },
    )
