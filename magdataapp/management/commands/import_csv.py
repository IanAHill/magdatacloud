from django.utils import timezone
import djclick as click
import csv

from magdataapp.models import *


def get_or_create_customer(**kwargs):
    # Normal example
    # try:
    #    customer = Customer.objects.get(customer_name=customer_name)
    # except Customer.DoesNotExist:
    #    customer = Customer.objects.create(customer_name=customer_name)

    # Easier helper way
    customer, created = Customer.objects.get_or_create(
        customer=kwargs["customer"],
        defaults={
            "created_time": kwargs.get("created_time", timezone.now()),
            "customer_name": kwargs.get("customer_name", "Uknown"),
            "customer_sub_type": kwargs.get("customer_sub_type", "BUSINESS"),
            "shipping_address": kwargs.get("shipping_address", "Uknown"),
            "shipping_city": kwargs.get("shipping_city", "Uknown"),
            "shipping_state": kwargs.get("shipping_state", "Uknown"),
            "shipping_code": kwargs.get("shipping_code", 0),
            "assigned_sales_person": kwargs.get("assigned_sales_person", "Uknown"),
            "state_manager": kwargs.get("state_manager", "Uknown"),
            "business_ein": kwargs.get("business_ein", "Uknown"),
            "tobacco_license": kwargs.get("tobacco_license", "Uknown"),
            "parent_chain": kwargs.get("parent_chain", "Uknown"),
        },
    )

    # If we want to update any fields about the customer we should do it here
    if not created:
        # Update fields here
        pass

    return customer


def get_or_create_invoice(**kwargs):
    invoice, created = Invoice.objects.get_or_create(
        invoice_number=kwargs["invoice_number"],
        customer=kwargs["customer"],
        defaults={
            "invoice": kwargs.get("invoice", 0),  # Bad default here
            "invoice_level_tax_authority": kwargs.get(
                "invoice_level_tax_authority", "Uknown"
            ),
            "invoice_date": kwargs.get("invoice_date", timezone.now()),
            "invoice_status": kwargs.get("invoice_status", "Uknown"),
        },
    )

    return invoice


@click.command()
@click.option(
    "--file-type",
    type=click.Choice(["CUSTOMERS", "ITEMS", "INVOICES"], case_sensitive=False),
    prompt=True,
)
@click.argument("filename", type=click.Path(exists=True))
def cli(file_type, filename):
    click.secho(f"Loading {filename}...", fg="green")

    with open(filename) as f:
        c = csv.reader(f)

        for i, row in enumerate(c):
            # Skip first row which are headers
            if i == 0:
                continue

            if file_type == "CUSTOMERS":
                #assign csv contents to variables to pass to the get_or_create_customer function. One csv line == 1 customer
                created_time = row[0]
                customer = row[1] ##the unique Zoho ID/Primary Key
                customer_name = row[2]
                customer_sub_type = row[3] #make sure default is set to business (in models, or kwargs?)
                taxable = row[4]
                customer_name = row[5]
                shipping_address = row[6]
                shipping_address_line_2 = row[7]
                shipping_city = row[8]
                shipping_state = row[9]
                shipping_code = row[10]
                assigned_sales_person = row[11]
                state_manager = row[12]
                business_ein = row[13]
                tobacco_license = row[14]
                parent_chain = row[15]
                customer_type = row[16]
                customer_pays_vape_tax = row[17]

                # Make customer
                customer = get_or_create_customer(
                    created_time = created_time,
                    customer = customer,  
                    customer_name=customer_name,
                    customer_sub_type = customer_sub_type,
                    taxable = taxable,
                    customer_name = customer_name,
                    shipping_address = shipping_address,
                    shipping_address_line_2 = shipping_address_line_2,
                    shipping_city = shipping_city,
                    shipping_state = shipping_state,
                    shipping_code = shipping_code,
                    assigned_sales_person = assigned_sales_person,
                    state_manager = state_manager,
                    business_ein = business_ein,
                    tobacco_license = tobacco_license,
                    parent_chain = parent_chain,
                    customer_type = customer_type,
                    customer_pays_vape_tax = customer_pays_vape_tax,
                )

            if file_type == "ITEMS":
                # Handle item info here to pass to line item
                # item = get_or_create_item(....)
                pass

            if file_type == "INVOICES":
                # Make invoice
                # `customer` here either needs to be the FK primary key in OUR database
                # or you need to retrieve it first by the data you have in the Invoice CSV file
                # If you're given the zoho ID do:
                # this_customer = Customer.objects.get(customer=zoho_id)

                invoice = get_or_create_invoice(
                    customer=this_customer,  # from above
                    invoice_number=invoice_number,
                    # rest of invoice kwargs here
                )

                # Get item here from invoice row data to pass to creating line items

                # Handle line item info here
                # line_item = get_or_create_line_item(item=item, invoice=invoice)
