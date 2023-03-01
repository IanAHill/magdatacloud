import djclick as click

from magdataapp.models import *


@click.command()
@click.argument("filename", type=click.Path(exists=True))
def cli(filename):
    print(filename)

    ####
    # Write csv import code here
    # customer, created = Customer.objects.get_or_create(...)
    # invoice, created = Invoice.objects.get_or_create(...)
    ####
