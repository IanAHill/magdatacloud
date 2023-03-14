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
            "customer_name": kwargs.get("customer_name", "Unknown"),
            "customer_sub_type": kwargs.get("customer_sub_type", "BUSINESS"),
            "shipping_address": kwargs.get("shipping_address", "Unknown"),
            "shipping_city": kwargs.get("shipping_city", "Unknown"),
            "shipping_state": kwargs.get("shipping_state", "Unknown"),
            "shipping_code": kwargs.get("shipping_code", 0),
            "assigned_sales_person": kwargs.get("assigned_sales_person", "Unknown"),
            "state_manager": kwargs.get("state_manager", "Unknown"),
            "business_ein": kwargs.get("business_ein", "Unknown"),
            "tobacco_license": kwargs.get("tobacco_license", "Unknown"),
            "parent_chain": kwargs.get("parent_chain", "Unknown"),
        },
    )

    # If we want to update any fields about the customer we should do it here
    if not created:
        # Update fields here
        pass

    return customer


def get_or_create_item(**kwargs):
    item, created = Item.objects.get_or_create(
        product = kwargs["product"],
        defaults = {
            "sku": kwargs.get("sku", "Unknown"),
            "item_name": kwargs.get("item_name", "Unknown"),
            "purchase_price": kwargs.get("purchase_price", 0.00),
            "preferred_vendor": kwargs.get("preferred_vendor", "Unknown"),
            "stock_on_hand": kwargs.get("stock_on_hand", 0),
            "category_name": kwargs.get("category_name", "Unknown"),
            "e_liquid_ml": kwargs.get("e_liquid_ml", 0.00),
            "msrp": kwargs.get("msrp", 0.00),
            "reporting_sub_category": kwargs.get("reporting_sub_category", "Unknown"),
            "reporting_category_primary": kwargs.get("reporting_category_primary", "Unknown"),
            "reporting_category_cannabinoid": kwargs.get("reporting_category_cannabinoid", "Unknown"),
            "cloud8_b2c": kwargs.get("cloud8_b2c", False),
            "b2c_msrp": kwargs.get("b2c_msrp", 0.00),
            "retail_units_in_wholesale": kwargs.get("retail_units_in_wholesale", 0),
            "OH_otp_tax": kwargs.get("OH_otp_tax", 0.00),
            "PA_otp_tax": kwargs.get("PA_otp_tax", 0.00),
            "WV_otp_tax": kwargs.get("WV_otp_tax", 0.00),
        },
    )
    if not created:
        # Update fields here
        pass

    return item



def get_or_create_invoice(**kwargs):
    invoice, created = Invoice.objects.get_or_create(
        invoice=kwargs["invoice"],
        customer=kwargs["customer"],
        defaults={
            "invoice_number": kwargs.get("invoice_number", "INV-Unknown"),  
            "invoice_level_tax_authority": kwargs.get("invoice_level_tax_authority", "Uknown"),
            "invoice_date": kwargs.get("invoice_date", timezone.now()),
            "invoice_status": kwargs.get("invoice_status", "Uknown"),
        },
    )

    return invoice


def get_or_create_line_item(**kwargs):
    line_item, created = Invoice_Line_Item.objects.get_or_create(
        invoice = kwargs["invoice"],
        item = kwargs["item"],
        defaults = {
            "quantity": kwargs.get("quantity", 0),
            "item_price": kwargs.get("item_price", 0.00),
            "item_total": kwargs.get("item_total", 0.00),
            "taxes_amount": kwargs.get("taxes_amount", 0.00),
            "total_sales": kwargs.get("total_sales", 0.00),
        },
    )

    return line_item



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
                product = row[0] #unique Zoho ID/Primary Key
                sku = row[1]
                item_name = row[2]
                purchase_price = row[3]
                preferred_vendor = row[4]
                stock_on_hand = row[5]
                category_name = row[6]
                e_liquid_ml = row[7]
                msrp = row[8]
                reporting_sub_category = row[9]
                reporting_category_primary = row[10]
                reporting_category_cannabinoid = row[11]
                cloud8_b2c = row[12]
                b2c_msrp = row[13]
                retail_units_in_wholesale = row[14]
                OH_otp_tax = row[15]
                PA_otp_tax = row[16]
                WV_otp_tax = row[17]

                item = get_or_create_item(
                    product = product,
                    sku = sku,
                    item_name = item_name,
                    purchase_price = purchase_price,
                    preferred_vendor = preferred_vendor,
                    stock_on_hand = stock_on_hand,
                    category_name = category_name,
                    e_liquid_ml = e_liquid_ml,
                    msrp = msrp,
                    reporting_sub_category = reporting_sub_category,
                    reporting_category_primary = reporting_category_primary,
                    reporting_category_cannabinoid = reporting_category_cannabinoid,
                    cloud8_b2c = cloud8_b2c,
                    b2c_msrp = b2c_msrp,
                    retail_units_in_wholesale = retail_units_in_wholesale,
                    OH_otp_tax = OH_otp_tax,
                    PA_otp_tax = PA_otp_tax,
                    WV_otp_tax = WV_otp_tax,
                )

        

            if file_type == "INVOICES":
                invoice_date = row[0]
                invoice = row[1]
                invoice_number = row[2]
                customer = row[3] #Unique Zoho ID/ Primary Key
                this_customer = Customer.objects.get(customer=customer)
                invoice_status = row[4]

                ##do NOT want to make a new invoice for every row in csv... one invoice has multiple line item rows
                invoice = get_or_create_invoice(
                    customer=this_customer,  
                    invoice_number=invoice_number,
                    invoice_date = invoice_date,
                    invoice = invoice,
                    invoice_status = invoice_status,
                )

                item = row[5]
                this_item = Item.objects.get(item=item)
                this_invoice = Invoice.objects.get(invoice=invoice) #referencing line 200
                quantity = row[5]
                item_price = row[6]
                item_total = row[7]
                taxes_amount = 0.00 ## this won't be on the csv... it's set by the calculate taxes function in taxes.py
                total_sales = 0.00 ## this won't be on the csv... it's set by the calculate taxes function in taxes.py

                line_item = get_or_create_line_item(

                )
                

                # Handle line item info here
                # line_item = get_or_create_line_item(item=item, invoice=invoice)
