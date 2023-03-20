from django.shortcuts import render
from .models import *
from .utils import get_plot

# Create your views here.
def home(request):
    qs = Invoice_Line_Item.objects.all()
    x = [x.item.item_name for x in qs]
    y = [y.item_total for y in qs]
    chart = get_plot(x, y)
    return render(request, "home.html", {'chart': chart})