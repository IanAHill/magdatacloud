import pytest

from magdataapp.models import *
from datetime import datetime
from magdataapp import taxes

def test_pytest():
    # Just to make sure pytest is up and working
    assert True


#def test_invalid_arguments():

   # with pytest.raises(ValueError):
   #     determine_tax_amount(state="PA")

# Equivalient to the above pytest.raises
#    failed = False
#    try:
#        determine_tax_amount(state="PA")
#    except ValueError:
#        failed = True
#
#    assert failed

   # with pytest.raises(ValueError):
       # determine_tax_amount(state="PA", ounces=3)


#def test_valid_arguments():
#    assert determine_tax_amount(state="PA", ounces=3, amount=10.01) == 0.00


def test_in_taxes(db):
    c1 = Customer.objects.create(
        created_time = datetime.now(),
        customer = 123456789,
        customer_sub_type = "BUSINESS",
        taxable = True,
        customer_name = "CStore",
        shipping_address = "123 Main Street",
        shipping_city = "Philadelphia",
        shipping_state = "PA",
        shipping_code = "07769",
        assigned_sales_person = "Shane",
        state_manager = "Zach",
        business_ein = "545641",
        tobacco_license = "15551 015",
        parent_chain = "CStore Master",
        customer_type = "CHAIN",
        customer_pays_vape_tax = True,
        )
    c2 = Customer.objects.create(
        created_time = datetime.now(),
        customer = 123456789,
        customer_sub_type = "BUSINESS",
        taxable = True,
        customer_name = "Klafters WV",
        shipping_address = "123 Main Street",
        shipping_city = "City",
        shipping_state = "WV",
        shipping_code = "07769",
        assigned_sales_person = "Shane",
        state_manager = "Zach",
        business_ein = "545641",
        tobacco_license = "15551 015",
        parent_chain = "CStore Master",
        customer_type = "CHAIN",
        customer_pays_vape_tax = True,
        )
    
    i1 = Item.objects.create(
        product = 123456789,
        sku = "HEMP47",
        item_name = "OG Kush 1ML Disposable Cart - 6CT",
        purchase_price = 4.75,
        preferred_vendor = "MAG Warehouse",
        stock_on_hand = 150,
        category_name = "Cloud 8",
        e_liquid_ml = 1.00,
        msrp = 29.99,
        reporting_sub_category = "1ML Disposable",
        reporting_category_primary = "Vapes",
        reporting_category_cannabinoid = "Delta 8",
        cloud8_b2c = True,
        b2c_msrp = 39.99,
        retail_units_in_wholesale = 6,
        OH_otp_tax = 0.00,
        PA_otp_tax = 0.00,
        WV_otp_tax = 0.00,
        )
    i2 = Item.objects.create(
        product = 123456789,
        sku = "SEN47",
        item_name = "American Club Pipe Tobacco",
        purchase_price = 11.00,
        preferred_vendor = "Seneca",
        stock_on_hand = 1150,
        category_name = "Rolling Tobacco",
        e_liquid_ml = 0.00,
        msrp = 127.99,
        ## only Cloud 8 Products have data for reporting categories
        reporting_sub_category = "",
        reporting_category_primary = "",
        reporting_category_cannabinoid = "",
        cloud8_b2c = False,
        b2c_msrp = null,
        retail_units_in_wholesale = 12,
        OH_otp_tax = 4.44,
        PA_otp_tax = 5.17,
        WV_otp_tax = 1.15,
        )
    i3 = Item.objects.create(
        product = 123456789,
        sku = "ELF55",
        item_name = "Elf Bar - Watermelon Breeze",
        purchase_price = 77.50,
        preferred_vendor = "Elf Bar",
        stock_on_hand = 950,
        category_name = "Disposable Vapes",
        e_liquid_ml = 130.00,
        msrp = 15.99,
        ## only Cloud 8 Products have data for reporting categories
        reporting_sub_category = "",
        reporting_category_primary = "",
        reporting_category_cannabinoid = "",
        cloud8_b2c = False,
        b2c_msrp = null,
        retail_units_in_wholesale = 10,
        OH_otp_tax = 0,
        PA_otp_tax = 0,
        WV_otp_tax = 0,
        )
    i4 = Item.objects.create(
        product = 123456789,
        sku = "BAD558",
        item_name = "Bad Drip - Bad Apple 60ml 3mg 1CT ",
        purchase_price = 6.00,
        preferred_vendor = "Bad Drip",
        stock_on_hand = 3950,
        category_name = "Vape Juice",
        e_liquid_ml = 60.00,
        msrp = 19.99,
        ## only Cloud 8 Products have data for reporting categories
        reporting_sub_category = "",
        reporting_category_primary = "",
        reporting_category_cannabinoid = "",
        cloud8_b2c = False,
        b2c_msrp = null,
        retail_units_in_wholesale = 1,
        OH_otp_tax = 0,
        PA_otp_tax = 0,
        WV_otp_tax = 0,
        )

    inv1 = Invoice.objects.create(
        invoice = 545456145,
        customer = c1,
        invoice_number = "INV-04738",
        invoice_level_tax_authority = "PA",
        invoice_date = datetime.today,
        invoice_status = "Closed",
    )
    inv2 = Invoice.objects.create(
        invoice = 533456145,
        customer = c2,
        invoice_number = "INV-04739",
        invoice_level_tax_authority = "WV",
        invoice_date = datetime.today,
        invoice_status = "Closed",
    )
    inv3 = Invoice.objects.create(
        invoice = 532226145,
        customer = c2,
        invoice_number = "INV-44739",
        invoice_level_tax_authority = "IN",
        invoice_date = datetime.today,
        invoice_status = "Closed",
    )
    inv4 = Invoice.objects.create(
        invoice = 532226145,
        customer = c2,
        invoice_number = "INV-44739",
        invoice_level_tax_authority = "KY",
        invoice_date = datetime.today,
        invoice_status = "Closed",
    )
    inv5 = Invoice.objects.create(
        invoice = 532226145,
        customer = c2,
        invoice_number = "INV-12569",
        invoice_level_tax_authority = "OH",
        invoice_date = datetime.today,
        invoice_status = "Closed",
    )


    l1 = Invoice_Line_Item.objects.create(
        invoice = inv1,
        item = i1,
        quantity = 3,
        item_price = 9.75,
        item_total = 9.75 * 3,
        taxes_amount = 0,
        total_sales = 0
    )
    l2 = Invoice_Line_Item.objects.create(
        invoice = inv1,
        item = i2,
        quantity = 2,
        item_price = 14.00,
        item_total = 28,
        taxes_amount = 0,
        total_sales = 0
    )
    l3 = Invoice_Line_Item.objects.create(
        invoice = inv2,
        item = i3,
        quantity = 2,
        item_price = 140.00,
        item_total = 280.00,
        taxes_amount = 0,
        total_sales = 0
    )
    
    taxes.extract_taxes(inv1)
    taxes.extract_taxes(inv2)

    inv1.refresh_from_db()
    inv2.refresh_from_db()
    l1.refresh_from_db()
    l2.refresh_from_db()
    l3.refresh_from_db()

    assert l1.total_sales == 0.00
    assert l1.taxes_amount == 0.00
    assert l2.taxes_amount == 0.00
    assert l3.taxes_amount == 0.00
