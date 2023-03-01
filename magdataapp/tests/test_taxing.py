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
        customer_pays_vape_tax = False,
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
        item_name = "Cloud 8 - Delta 8 -OG Kush - 1ML Cartridge - 6CT",
        purchase_price = 20.59,
        preferred_vendor = "MAG Warehouse",
        stock_on_hand = 150,
        category_name = "Cloud 8",
        e_liquid_ml = 6.00,
        msrp = 19.99,
        reporting_sub_category = "1ML Cartridge",
        reporting_category_primary = "Vapes",
        reporting_category_cannabinoid = "Delta 8",
        cloud8_b2c = True,
        b2c_msrp = 29.99,
        retail_units_in_wholesale = 6,
        OH_otp_tax = 0.00,
        PA_otp_tax = 0.00,
        WV_otp_tax = 0.00,
        )
    i2 = Item.objects.create(
        product = 123456789,
        sku = "SEN47",
        item_name = "American Club Expanded Pipe Tobacco - Menthol - 16oz -1ct",
        purchase_price = 7.00,
        preferred_vendor = "Seneca",
        stock_on_hand = 1150,
        category_name = "Rolling Tobacco",
        e_liquid_ml = 0.00,
        msrp = 13.99,
        ## only Cloud 8 Products have data for reporting categories
        reporting_sub_category = "",
        reporting_category_primary = "",
        reporting_category_cannabinoid = "",
        cloud8_b2c = False,
        #b2c_msrp = null,
        retail_units_in_wholesale = 1,
        OH_otp_tax = 1.19,
        PA_otp_tax = 8.80,
        WV_otp_tax = 0.84,
        )
    i3 = Item.objects.create(
        product = 123456789,
        sku = "ELF55",
        item_name = "Elf Bar bc5000 Disposable - 5000 Puff - Strawberry Mango - 13ML - 10CT Carton (not returnable)",
        purchase_price = 85.70,
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
        #b2c_msrp = null,
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
        #b2c_msrp = null,
        retail_units_in_wholesale = 1,
        OH_otp_tax = 0,
        PA_otp_tax = 0,
        WV_otp_tax = 0,
        )
    i5 = Item.objects.create(
        product = 4654687486,
        sku = "HEMPMERCH45",
        item_name = "Cloud 8 T Shirt - Large",
        purchase_price = 4.00,
        preferred_vendor = "MAG Warehouse",
        stock_on_hand = 50,
        category_name = "Cloud 8 - Marketing Materials",
        e_liquid_ml = 0.00,
        msrp = 7.99,
        reporting_sub_category = "",
        reporting_category_primary = "",
        reporting_category_cannabinoid = "",
        cloud8_b2c = False,
        #b2c_msrp = null,
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
        invoice_date = datetime.today(),
        invoice_status = "Closed",
    )
    inv2 = Invoice.objects.create(
        invoice = 533456145,
        customer = c2,
        invoice_number = "INV-04739",
        invoice_level_tax_authority = "WV",
        invoice_date = datetime.today(),
        invoice_status = "Closed",
    )
    inv3 = Invoice.objects.create(
        invoice = 532226145,
        customer = c1,
        invoice_number = "INV-44739",
        invoice_level_tax_authority = "IN",
        invoice_date = datetime.today(),
        invoice_status = "Closed",
    )
    inv4 = Invoice.objects.create(
        invoice = 532226145,
        customer = c2,
        invoice_number = "INV-44739",
        invoice_level_tax_authority = "KY",
        invoice_date = datetime.today(),
        invoice_status = "Closed",
    )
    inv5 = Invoice.objects.create(
        invoice = 532226145,
        customer = c1,
        invoice_number = "INV-12569",
        invoice_level_tax_authority = "OH",
        invoice_date = datetime.today(),
        invoice_status = "Closed",
    )
    inv6 = Invoice.objects.create(
        invoice = 5322244145,
        customer = c2,
        invoice_number = "INV-02569",
        invoice_level_tax_authority = "NJ",
        invoice_date = datetime.today(),
        invoice_status = "Closed",
    )
    inv7 = Invoice.objects.create(
        invoice = 5322244145,
        customer = c1,
        invoice_number = "INV-02569",
        invoice_level_tax_authority = "IL",
        invoice_date = datetime.today(),
        invoice_status = "Closed",
    )
    inv8 = Invoice.objects.create(
        invoice = 5322244145,
        customer = c2,
        invoice_number = "INV-02569",
        invoice_level_tax_authority = "FL",
        invoice_date = datetime.today(),
        invoice_status = "Closed",
    )

#Invoice 1 Line Items
    l1 = Invoice_Line_Item.objects.create(
        invoice = inv1,
        item = i1,
        quantity = 3,
        item_price = 60.00,
        item_total = 60.00 * 3,
        taxes_amount = 0,
        total_sales = 0
    )
    l2 = Invoice_Line_Item.objects.create(
        invoice = inv1,
        item = i2,
        quantity = 2,
        item_price = 9.00,
        item_total = 18,
        taxes_amount = 0,
        total_sales = 0
    )
    l3 = Invoice_Line_Item.objects.create(
        invoice = inv1,
        item = i3,
        quantity = 2,
        item_price = 107.50,
        item_total = 215.00,
        taxes_amount = 0,
        total_sales = 0
    )
    l4 = Invoice_Line_Item.objects.create(
        invoice = inv1,
        item = i4,
        quantity = 1,
        item_price = 10.00,
        item_total = 10.00,
        taxes_amount = 0,
        total_sales = 0
    )
    l5 = Invoice_Line_Item.objects.create(
        invoice = inv1,
        item = i5,
        quantity = 1,
        item_price = 5.00,
        item_total = 5.00,
        taxes_amount = 0,
        total_sales = 0
    )
#Invoice 2 Line Items
    l6 = Invoice_Line_Item.objects.create(
        invoice = inv2,
        item = i1,
        quantity = 3,
        item_price = 60.00,
        item_total = 60.00 * 3,
        taxes_amount = 0,
        total_sales = 0
    )
    l7 = Invoice_Line_Item.objects.create(
        invoice = inv2,
        item = i2,
        quantity = 2,
        item_price = 9.00,
        item_total = 18,
        taxes_amount = 0,
        total_sales = 0
    )
    l8 = Invoice_Line_Item.objects.create(
        invoice = inv2,
        item = i3,
        quantity = 2,
        item_price = 107.50,
        item_total = 215.00,
        taxes_amount = 0,
        total_sales = 0
    )
    l9 = Invoice_Line_Item.objects.create(
        invoice = inv2,
        item = i4,
        quantity = 1,
        item_price = 10.00,
        item_total = 10.00,
        taxes_amount = 0,
        total_sales = 0
    )
    l10 = Invoice_Line_Item.objects.create(
        invoice = inv2,
        item = i5,
        quantity = 1,
        item_price = 5.00,
        item_total = 5.00,
        taxes_amount = 0,
        total_sales = 0
    )
#Invoice 3 Line Items
    l11 = Invoice_Line_Item.objects.create(
        invoice = inv3,
        item = i1,
        quantity = 3,
        item_price = 60.00,
        item_total = 60.00 * 3,
        taxes_amount = 0,
        total_sales = 0
    )
    l12 = Invoice_Line_Item.objects.create(
        invoice = inv3,
        item = i2,
        quantity = 2,
        item_price = 9.00,
        item_total = 18,
        taxes_amount = 0,
        total_sales = 0
    )
    l13 = Invoice_Line_Item.objects.create(
        invoice = inv3,
        item = i3,
        quantity = 2,
        item_price = 107.50,
        item_total = 215.00,
        taxes_amount = 0,
        total_sales = 0
    )
    l14 = Invoice_Line_Item.objects.create(
        invoice = inv3,
        item = i4,
        quantity = 1,
        item_price = 10.00,
        item_total = 10.00,
        taxes_amount = 0,
        total_sales = 0
    )
    l15 = Invoice_Line_Item.objects.create(
        invoice = inv3,
        item = i5,
        quantity = 1,
        item_price = 5.00,
        item_total = 5.00,
        taxes_amount = 0,
        total_sales = 0
    )
#Invoice 4 Line Items
    l16 = Invoice_Line_Item.objects.create(
        invoice = inv4,
        item = i1,
        quantity = 3,
        item_price = 60.00,
        item_total = 60.00 * 3,
        taxes_amount = 0,
        total_sales = 0
    )
    l17 = Invoice_Line_Item.objects.create(
        invoice = inv4,
        item = i2,
        quantity = 2,
        item_price = 9.00,
        item_total = 18,
        taxes_amount = 0,
        total_sales = 0
    )
    l18 = Invoice_Line_Item.objects.create(
        invoice = inv4,
        item = i3,
        quantity = 2,
        item_price = 107.50,
        item_total = 215.00,
        taxes_amount = 0,
        total_sales = 0
    )
    l19 = Invoice_Line_Item.objects.create(
        invoice = inv4,
        item = i4,
        quantity = 1,
        item_price = 10.00,
        item_total = 10.00,
        taxes_amount = 0,
        total_sales = 0
    )
    l20 = Invoice_Line_Item.objects.create(
        invoice = inv4,
        item = i5,
        quantity = 1,
        item_price = 5.00,
        item_total = 5.00,
        taxes_amount = 0,
        total_sales = 0
    )
#Invoice 5 Line Items
    l21 = Invoice_Line_Item.objects.create(
        invoice = inv5,
        item = i1,
        quantity = 3,
        item_price = 60.00,
        item_total = 60.00 * 3,
        taxes_amount = 0,
        total_sales = 0
    )
    l22 = Invoice_Line_Item.objects.create(
        invoice = inv5,
        item = i2,
        quantity = 2,
        item_price = 9.00,
        item_total = 18,
        taxes_amount = 0,
        total_sales = 0
    )
    l23 = Invoice_Line_Item.objects.create(
        invoice = inv5,
        item = i3,
        quantity = 2,
        item_price = 107.50,
        item_total = 215.00,
        taxes_amount = 0,
        total_sales = 0
    )
    l24 = Invoice_Line_Item.objects.create(
        invoice = inv5,
        item = i4,
        quantity = 1,
        item_price = 10.00,
        item_total = 10.00,
        taxes_amount = 0,
        total_sales = 0
    )
    l25 = Invoice_Line_Item.objects.create(
        invoice = inv5,
        item = i5,
        quantity = 1,
        item_price = 5.00,
        item_total = 5.00,
        taxes_amount = 0,
        total_sales = 0
    )
#Invoice 6 Line Items
    l26 = Invoice_Line_Item.objects.create(
        invoice = inv6,
        item = i1,
        quantity = 3,
        item_price = 60.00,
        item_total = 60.00 * 3,
        taxes_amount = 0,
        total_sales = 0
    )
    l27 = Invoice_Line_Item.objects.create(
        invoice = inv6,
        item = i2,
        quantity = 2,
        item_price = 9.00,
        item_total = 18,
        taxes_amount = 0,
        total_sales = 0
    )
    l28 = Invoice_Line_Item.objects.create(
        invoice = inv6,
        item = i3,
        quantity = 2,
        item_price = 107.50,
        item_total = 215.00,
        taxes_amount = 0,
        total_sales = 0
    )
    l29 = Invoice_Line_Item.objects.create(
        invoice = inv6,
        item = i4,
        quantity = 1,
        item_price = 10.00,
        item_total = 10.00,
        taxes_amount = 0,
        total_sales = 0
    )
    l30 = Invoice_Line_Item.objects.create(
        invoice = inv6,
        item = i5,
        quantity = 1,
        item_price = 5.00,
        item_total = 5.00,
        taxes_amount = 0,
        total_sales = 0
    )
#Invoice 7 Line Items
    l31 = Invoice_Line_Item.objects.create(
        invoice = inv7,
        item = i1,
        quantity = 3,
        item_price = 60.00,
        item_total = 60.00 * 3,
        taxes_amount = 0,
        total_sales = 0
    )
    l32 = Invoice_Line_Item.objects.create(
        invoice = inv7,
        item = i2,
        quantity = 2,
        item_price = 9.00,
        item_total = 18,
        taxes_amount = 0,
        total_sales = 0
    )
    l33 = Invoice_Line_Item.objects.create(
        invoice = inv7,
        item = i3,
        quantity = 2,
        item_price = 107.50,
        item_total = 215.00,
        taxes_amount = 0,
        total_sales = 0
    )
    l34 = Invoice_Line_Item.objects.create(
        invoice = inv7,
        item = i4,
        quantity = 1,
        item_price = 10.00,
        item_total = 10.00,
        taxes_amount = 0,
        total_sales = 0
    )
    l35 = Invoice_Line_Item.objects.create(
        invoice = inv7,
        item = i5,
        quantity = 1,
        item_price = 5.00,
        item_total = 5.00,
        taxes_amount = 0,
        total_sales = 0
    )
#Invoice 8 Line Items
    l36 = Invoice_Line_Item.objects.create(
        invoice = inv8,
        item = i1,
        quantity = 3,
        item_price = 60.00,
        item_total = 60.00 * 3,
        taxes_amount = 0,
        total_sales = 0
    )
    l37 = Invoice_Line_Item.objects.create(
        invoice = inv8,
        item = i2,
        quantity = 2,
        item_price = 9.00,
        item_total = 18,
        taxes_amount = 0,
        total_sales = 0
    )
    l38 = Invoice_Line_Item.objects.create(
        invoice = inv8,
        item = i3,
        quantity = 2,
        item_price = 107.50,
        item_total = 215.00,
        taxes_amount = 0,
        total_sales = 0
    )
    l39 = Invoice_Line_Item.objects.create(
        invoice = inv8,
        item = i4,
        quantity = 1,
        item_price = 10.00,
        item_total = 10.00,
        taxes_amount = 0,
        total_sales = 0
    )
    l40 = Invoice_Line_Item.objects.create(
        invoice = inv8,
        item = i5,
        quantity = 1,
        item_price = 5.00,
        item_total = 5.00,
        taxes_amount = 0,
        total_sales = 0
    )



    taxes.extract_taxes(inv1)
    taxes.extract_taxes(inv2)
    taxes.extract_taxes(inv3)
    taxes.extract_taxes(inv4)
    taxes.extract_taxes(inv5)
    taxes.extract_taxes(inv6)
    taxes.extract_taxes(inv7)
    taxes.extract_taxes(inv8)


    inv1.refresh_from_db()
    inv2.refresh_from_db()
    inv3.refresh_from_db()
    inv4.refresh_from_db()
    inv5.refresh_from_db()
    inv6.refresh_from_db()
    inv7.refresh_from_db()
    inv8.refresh_from_db()
    l1.refresh_from_db()
    l2.refresh_from_db()
    l3.refresh_from_db()
    l4.refresh_from_db()
    l5.refresh_from_db()
    l6.refresh_from_db()
    l7.refresh_from_db()
    l8.refresh_from_db()
    l9.refresh_from_db()
    l10.refresh_from_db()
    l11.refresh_from_db()
    l12.refresh_from_db()
    l13.refresh_from_db()
    l14.refresh_from_db()
    l15.refresh_from_db()
    l16.refresh_from_db()
    l17.refresh_from_db()
    l18.refresh_from_db()
    l19.refresh_from_db()
    l20.refresh_from_db()
    l21.refresh_from_db()
    l22.refresh_from_db()
    l23.refresh_from_db()
    l24.refresh_from_db()
    l25.refresh_from_db()
    l26.refresh_from_db()
    l27.refresh_from_db()
    l28.refresh_from_db()
    l29.refresh_from_db()
    l30.refresh_from_db()
    l31.refresh_from_db()
    l32.refresh_from_db()
    l33.refresh_from_db()
    l34.refresh_from_db()
    l35.refresh_from_db()
    l36.refresh_from_db()
    l37.refresh_from_db()
    l38.refresh_from_db()
    l39.refresh_from_db()
    l40.refresh_from_db()


    #assert l1.total_sales == 180
    assert l1.taxes_amount == 0
    assert l2.total_sales == .4
    assert l2.taxes_amount == 17.6
    assert l3.total_sales == 215
    assert l3.taxes_amount == 0
    assert l4.total_sales == 10
    assert l4.taxes_amount == 0
    assert l5.total_sales == 5
    assert l5.taxes_amount == 0
    assert l6.total_sales == 178.65
    assert l6.taxes_amount == 1.35
    assert l7.total_sales == 16.32
    assert l7.taxes_amount == 1.68
    assert l8.total_sales == 195.5
    assert l8.taxes_amount == 19.5
    assert l9.total_sales == 5.50
    assert l9.taxes_amount == 4.50
    assert l10.total_sales == 5
    assert l10.taxes_amount == 0
    assert l11.total_sales == 170.7345
    assert l11.taxes_amount == 9.2655
    assert l12.total_sales == 18
    assert l12.taxes_amount == 0
    assert l13.total_sales == 189.29
    assert l13.taxes_amount == 25.71
    assert l14.total_sales == 9.10
    assert l14.taxes_amount == .90
    assert l15.total_sales == 5
    assert l15.taxes_amount == 0
    assert l16.total_sales == 153
    assert l16.taxes_amount == 27
    assert l17.total_sales == 18
    assert l17.taxes_amount == 0
    assert l18.total_sales == 185
    assert l18.taxes_amount == 30
    assert l19.total_sales == 8.69565217
    assert l19.taxes_amount == 1.304347826
    assert l20.total_sales == 5
    assert l20.taxes_amount == 0
    assert l21.total_sales == 180
    assert l21.taxes_amount == 0
    assert l22.total_sales == 15.62
    assert l22.taxes_amount == 2.38
    assert l23.total_sales == 189
    assert l23.taxes_amount == 26
    assert l24.total_sales == 4
    assert l24.taxes_amount == 6
    assert l25.total_sales == 5
    assert l25.taxes_amount == 0
    assert l26.total_sales == 180
    assert l26.taxes_amount == 0
    assert l27.total_sales == 18
    assert l27.taxes_amount == 0
    assert l28.total_sales == 215
    assert l28.taxes_amount == 0
    assert l29.total_sales == 10
    assert l29.taxes_amount == 0
    assert l30.total_sales == 5
    assert l30.taxes_amount == 0
    assert l31.total_sales == 170.7345
    assert l31.taxes_amount == 9.2655
    assert l32.total_sales == 18
    assert l32.taxes_amount == 0
    assert l33.total_sales == 189.29
    assert l33.taxes_amount == 25.71
    assert l34.total_sales == 9.10
    assert l34.taxes_amount == .9
    assert l35.total_sales == 5
    assert l35.taxes_amount == 0
    assert l36.total_sales == 180
    assert l36.taxes_amount == 0
    assert l37.total_sales == 18
    assert l37.taxes_amount == 0
    assert l38.total_sales == 215
    assert l38.taxes_amount == 0
    assert l39.total_sales == 10
    assert l39.taxes_amount == 0
    assert l40.total_sales == 5
    assert l40.taxes_amount == 0
