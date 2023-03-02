import djclick as click
import csv

from magdataapp.models import *


@click.command()
@click.argument("filename", type=click.Path(exists=True))
def cli(filename):
    print(filename)




    with open('invoice.csv') as invoice_csv:
        invoice_data = invoice_csv.readlines()
    
    for line in invoice_data:
        line_item = Invoice_Line_Item.objects.get_or_create()
        pass
    ####
    # Write csv import code here
    # customer, created = Customer.objects.get_or_create(...)
    # invoice, created = Invoice.objects.get_or_create(...)
    ####
