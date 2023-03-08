import pytest

from decimal import Decimal
from magdataapp.models import *
from datetime import datetime
from magdataapp import taxes


def test_pytest():
    # Just to make sure pytest is up and working
    assert True


@pytest.fixture
def customer(db):
    return Customer.objects.create(
        created_time=datetime.now(),
        customer=123456789,
        customer_sub_type="BUSINESS",
        taxable=True,
        customer_name="CStore",
        shipping_address="123 Main Street",
        shipping_city="Philadelphia",
        shipping_state="PA",
        shipping_code="07769",
        assigned_sales_person="Shane",
        state_manager="Zach",
        business_ein="545641",
        tobacco_license="15551 015",
        parent_chain="CStore Master",
        customer_type="CHAIN",
        customer_pays_vape_tax=False,
    )


@pytest.fixture
def disposable_vape(db):
    return Item.objects.create(
        product=123456789,
        sku="ELF55",
        item_name="Elf Bar bc5000 Disposable - 5000 Puff - Strawberry Mango - 13ML - 10CT Carton (not returnable)",
        purchase_price=85.70,
        preferred_vendor="Elf Bar",
        stock_on_hand=950,
        category_name="Disposable Vapes",
        e_liquid_ml=130.00,
        msrp=15.99,
        ## only Cloud 8 Products have data for reporting categories
        reporting_sub_category="",
        reporting_category_primary="",
        reporting_category_cannabinoid="",
        cloud8_b2c=False,
        # b2c_msrp = null,
        retail_units_in_wholesale=10,
        OH_otp_tax=0,
        PA_otp_tax=0,
        WV_otp_tax=0,
    )


@pytest.fixture
def matching_cloud8(db):
    return Item.objects.create(
        product=123456789,
        sku="MATCHHEMP47",
        item_name="Cloud 8 - Delta 8 -OG Kush - 1ML Cartridge - 6CT",
        purchase_price=20.59,
        preferred_vendor="MAG Warehouse",
        stock_on_hand=150,
        category_name="Cloud 8",
        e_liquid_ml=6.00,
        msrp=19.99,
        reporting_sub_category="1ML Cartridge",
        reporting_category_primary="Vapes",
        reporting_category_cannabinoid="Delta 8",
        cloud8_b2c=True,
        b2c_msrp=29.99,
        retail_units_in_wholesale=6,
        OH_otp_tax=0.00,
        PA_otp_tax=0.00,
        WV_otp_tax=0.00,
    )


@pytest.fixture
def not_matching_cloud8(db):
    return Item.objects.create(
        product=123456789,
        sku="NOMATCHHEMP47",
        item_name="Cloud 8 - Delta 8 -OG Kush - 1ML Cartridge - 6CT",
        purchase_price=20.59,
        preferred_vendor="MAG Warehouse",
        stock_on_hand=150,
        category_name="Cloud 8",
        e_liquid_ml=6.00,
        msrp=19.99,
        reporting_sub_category="DOES NOT MATCH",
        reporting_category_primary="Vapes",
        reporting_category_cannabinoid="Delta 8",
        cloud8_b2c=True,
        b2c_msrp=29.99,
        retail_units_in_wholesale=6,
        OH_otp_tax=0.00,
        PA_otp_tax=0.00,
        WV_otp_tax=0.00,
    )

@pytest.fixture
def otp_item(db):
    return Item.objects.create(
        product=123456789,
        sku="CLUB14",
        item_name="AMERICAN CLUB - pipe tobacco",
        purchase_price=7.00,
        preferred_vendor="MAG Warehouse",
        stock_on_hand=150,
        category_name="Rolling Tobacco",
        e_liquid_ml=0.00,
        msrp=19.99,
        reporting_sub_category="",
        reporting_category_primary="",
        reporting_category_cannabinoid="",
        cloud8_b2c=False,
        b2c_msrp=29.99,
        retail_units_in_wholesale=1,
        OH_otp_tax=1.19,
        PA_otp_tax=8.80,
        WV_otp_tax=0.84,
    )

@pytest.fixture
def vape_juice(db):
    return Item.objects.create(
        product=12345673489,
        sku="BAD454",
        item_name="Bad Drip Strawberry Watermelon",
        purchase_price=6.00,
        preferred_vendor="MAG Warehouse",
        stock_on_hand=150,
        category_name="Vape Juice",
        e_liquid_ml=60.00,
        msrp=19.99,
        reporting_sub_category="",
        reporting_category_primary="",
        reporting_category_cannabinoid="",
        cloud8_b2c=False,
        b2c_msrp=29.99,
        retail_units_in_wholesale=1,
        OH_otp_tax=0.00,
        PA_otp_tax=0.00,
        WV_otp_tax=0.00,
    )


@pytest.fixture
def no_tax_product(db):
    return Item.objects.create(
        product=5551234,
        sku="NO TAX HEMP47",
        item_name="Cloud 8 - Delta 8 -OG Kush - 1ML Cartridge - 6CT",
        purchase_price=20.59,
        preferred_vendor="MAG Warehouse",
        stock_on_hand=150,
        category_name="NO TAX",
        e_liquid_ml=0.00,
        msrp=19.99,
        reporting_sub_category="DOES NOT MATCH",
        reporting_category_primary="Vapes",
        reporting_category_cannabinoid="Delta 8",
        cloud8_b2c=True,
        b2c_msrp=29.99,
        retail_units_in_wholesale=6,
        OH_otp_tax=0.00,
        PA_otp_tax=0.00,
        WV_otp_tax=0.00,
    )


@pytest.fixture
def invoice(
    customer, disposable_vape, matching_cloud8, not_matching_cloud8, no_tax_product, otp_item, vape_juice
):
    inv = Invoice.objects.create(
        invoice=10545456145,
        customer=customer,
        invoice_number="INV-04738",
        invoice_level_tax_authority="KS",
        invoice_date=datetime.today(),
        invoice_status="Closed",
    )
    l1 = Invoice_Line_Item.objects.create(
        invoice=inv,
        item=disposable_vape,
        quantity=2,
        item_price=107.50,
        item_total=215.00,
        taxes_amount=0,
        total_sales=0,
    )
    l2 = Invoice_Line_Item.objects.create(
        invoice=inv,
        item=matching_cloud8,
        quantity=3,
        item_price=60,
        item_total=180,
        taxes_amount=0,
        total_sales=0,
    )
    l3 = Invoice_Line_Item.objects.create(
        invoice=inv,
        item=not_matching_cloud8,
        quantity=2,
        item_price=107.50,
        item_total=215.00,
        taxes_amount=0,
        total_sales=0,
    )
    l4 = Invoice_Line_Item.objects.create(
        invoice=inv,
        item=no_tax_product,
        quantity=1,
        item_price=5.00,
        item_total=5.00,
        taxes_amount=0,
        total_sales=0,
    )
    l5 = Invoice_Line_Item.objects.create(
        invoice=inv,
        item=otp_item,
        quantity = 2,
        item_price = 9.00,
        item_total = 18,
        taxes_amount=0,
        total_sales = 0,
    )
    l6 = Invoice_Line_Item.objects.create(
        invoice=inv,
        item=vape_juice,
        quantity = 1,
        item_price = 10.00,
        item_total = 10.00,
        taxes_amount=0,
        total_sales = 0,
    )

    return inv



def test_indiana_taxes(
    invoice, disposable_vape, matching_cloud8, not_matching_cloud8, no_tax_product, vape_juice, otp_item
):
    invoice.invoice_level_tax_authority = "IN"
    invoice.save()
    taxes.extract_taxes(invoice)
    invoice.refresh_from_db()

    inv_disposable_vape = invoice.line_items.get(item=disposable_vape)
    assert inv_disposable_vape.total_sales == Decimal("189.29")
    assert inv_disposable_vape.taxes_amount == Decimal("25.71")

    inv_matching_cloud8 = invoice.line_items.get(item=matching_cloud8)
    assert inv_matching_cloud8.total_sales == Decimal("170.7345")
    assert inv_matching_cloud8.taxes_amount == Decimal("9.2655")

    inv_not_matching_cloud8 = invoice.line_items.get(item=not_matching_cloud8)
    assert inv_not_matching_cloud8.total_sales == Decimal("215.00")
    assert inv_not_matching_cloud8.taxes_amount == Decimal("0.00")

    inv_no_tax_product = invoice.line_items.get(item=no_tax_product)
    assert inv_no_tax_product.total_sales == Decimal("5.00")
    assert inv_no_tax_product.taxes_amount == Decimal("0.00")

    inv_vape_juice = invoice.line_items.get(item=vape_juice)
    assert inv_vape_juice.total_sales == Decimal("10.00")
    assert inv_vape_juice.taxes_amount == Decimal("0.00")

    inv_otp_item = invoice.line_items.get(item=otp_item)
    assert inv_otp_item.total_sales == Decimal("18.00")
    assert inv_otp_item.taxes_amount == Decimal("0.00")



def test_pa_taxes(
    invoice, disposable_vape, matching_cloud8, not_matching_cloud8, no_tax_product, vape_juice, otp_item
):
    invoice.invoice_level_tax_authority = "PA"
    invoice.save()
    taxes.extract_taxes(invoice)
    invoice.refresh_from_db()

    inv_disposable_vape = invoice.line_items.get(item=disposable_vape)
    assert inv_disposable_vape.total_sales == Decimal("215")
    assert inv_disposable_vape.taxes_amount == Decimal("0.00")

    inv_matching_cloud8 = invoice.line_items.get(item=matching_cloud8)
    assert inv_matching_cloud8.total_sales == Decimal("180")
    assert inv_matching_cloud8.taxes_amount == Decimal("0.00")

    inv_not_matching_cloud8 = invoice.line_items.get(item=not_matching_cloud8)
    assert inv_not_matching_cloud8.total_sales == Decimal("215")
    assert inv_not_matching_cloud8.taxes_amount == Decimal("0.00")

    inv_no_tax_product = invoice.line_items.get(item=no_tax_product)
    assert inv_no_tax_product.total_sales == Decimal("5.00")
    assert inv_no_tax_product.taxes_amount == Decimal("0.00")

    inv_vape_juice = invoice.line_items.get(item=vape_juice)
    assert inv_vape_juice.total_sales == Decimal("10.00")
    assert inv_vape_juice.taxes_amount == Decimal("0.00")

    inv_otp_item = invoice.line_items.get(item=otp_item)
    assert inv_otp_item.total_sales == Decimal("0.40")
    assert inv_otp_item.taxes_amount == Decimal("17.60")



def test_wv_taxes(
    invoice, disposable_vape, matching_cloud8, not_matching_cloud8, no_tax_product, vape_juice, otp_item
):
    invoice.invoice_level_tax_authority = "WV"
    invoice.save()
    taxes.extract_taxes(invoice)
    invoice.refresh_from_db()

    inv_disposable_vape = invoice.line_items.get(item=disposable_vape)
    assert inv_disposable_vape.total_sales == Decimal("195.50")
    assert inv_disposable_vape.taxes_amount == Decimal("19.50")

    inv_matching_cloud8 = invoice.line_items.get(item=matching_cloud8)
    assert inv_matching_cloud8.total_sales == Decimal("178.65")
    assert inv_matching_cloud8.taxes_amount == Decimal("1.35")

    inv_not_matching_cloud8 = invoice.line_items.get(item=not_matching_cloud8)
    assert inv_not_matching_cloud8.total_sales == Decimal("215")
    assert inv_not_matching_cloud8.taxes_amount == Decimal("0.00")

    inv_no_tax_product = invoice.line_items.get(item=no_tax_product)
    assert inv_no_tax_product.total_sales == Decimal("5.00")
    assert inv_no_tax_product.taxes_amount == Decimal("0.00")

    inv_vape_juice = invoice.line_items.get(item=vape_juice)
    assert inv_vape_juice.total_sales == Decimal("5.50")
    assert inv_vape_juice.taxes_amount == Decimal("4.50")

    inv_otp_item = invoice.line_items.get(item=otp_item)
    assert inv_otp_item.total_sales == Decimal("16.32")
    assert inv_otp_item.taxes_amount == Decimal("1.68")


def test_ky_taxes(
    invoice, disposable_vape, matching_cloud8, not_matching_cloud8, no_tax_product, vape_juice, otp_item
):
    invoice.invoice_level_tax_authority = "KY"
    invoice.save()
    taxes.extract_taxes(invoice)
    invoice.refresh_from_db()

    inv_disposable_vape = invoice.line_items.get(item=disposable_vape)
    assert inv_disposable_vape.total_sales == Decimal("185.00")
    assert inv_disposable_vape.taxes_amount == Decimal("30.00")

    inv_matching_cloud8 = invoice.line_items.get(item=matching_cloud8)
    assert inv_matching_cloud8.total_sales == Decimal("153.00")
    assert inv_matching_cloud8.taxes_amount == Decimal("27.00")

    inv_not_matching_cloud8 = invoice.line_items.get(item=not_matching_cloud8)
    assert inv_not_matching_cloud8.total_sales == Decimal("215")
    assert inv_not_matching_cloud8.taxes_amount == Decimal("0.00")

    inv_no_tax_product = invoice.line_items.get(item=no_tax_product)
    assert inv_no_tax_product.total_sales == Decimal("5.00")
    assert inv_no_tax_product.taxes_amount == Decimal("0.00")

    inv_vape_juice = invoice.line_items.get(item=vape_juice)
    assert inv_vape_juice.total_sales == Decimal("8.69565217")
    assert inv_vape_juice.taxes_amount == Decimal("1.304347826")

    inv_otp_item = invoice.line_items.get(item=otp_item)
    assert inv_otp_item.total_sales == Decimal("18.00")
    assert inv_otp_item.taxes_amount == Decimal("0.00")


def test_oh_taxes(
    invoice, disposable_vape, matching_cloud8, not_matching_cloud8, no_tax_product, vape_juice, otp_item
):
    invoice.invoice_level_tax_authority = "OH"
    invoice.save()
    taxes.extract_taxes(invoice)
    invoice.refresh_from_db()

    inv_disposable_vape = invoice.line_items.get(item=disposable_vape)
    assert inv_disposable_vape.total_sales == Decimal("189.00")
    assert inv_disposable_vape.taxes_amount == Decimal("26.00")

    inv_matching_cloud8 = invoice.line_items.get(item=matching_cloud8)
    assert inv_matching_cloud8.total_sales == Decimal("180.00")
    assert inv_matching_cloud8.taxes_amount == Decimal("0.00")

    inv_not_matching_cloud8 = invoice.line_items.get(item=not_matching_cloud8)
    assert inv_not_matching_cloud8.total_sales == Decimal("215")
    assert inv_not_matching_cloud8.taxes_amount == Decimal("0.00")

    inv_no_tax_product = invoice.line_items.get(item=no_tax_product)
    assert inv_no_tax_product.total_sales == Decimal("5.00")
    assert inv_no_tax_product.taxes_amount == Decimal("0.00")

    inv_vape_juice = invoice.line_items.get(item=vape_juice)
    assert inv_vape_juice.total_sales == Decimal("4.00")
    assert inv_vape_juice.taxes_amount == Decimal("6.00")

    inv_otp_item = invoice.line_items.get(item=otp_item)
    assert inv_otp_item.total_sales == Decimal("15.62")
    assert inv_otp_item.taxes_amount == Decimal("2.38")



def test_nj_taxes(
    invoice, disposable_vape, matching_cloud8, not_matching_cloud8, no_tax_product, vape_juice, otp_item
):
    invoice.invoice_level_tax_authority = "NJ"
    invoice.save()
    taxes.extract_taxes(invoice)
    invoice.refresh_from_db()

    inv_disposable_vape = invoice.line_items.get(item=disposable_vape)
    assert inv_disposable_vape.total_sales == Decimal("215.00")
    assert inv_disposable_vape.taxes_amount == Decimal("0.00")

    inv_matching_cloud8 = invoice.line_items.get(item=matching_cloud8)
    assert inv_matching_cloud8.total_sales == Decimal("180.00")
    assert inv_matching_cloud8.taxes_amount == Decimal("0.00")

    inv_not_matching_cloud8 = invoice.line_items.get(item=not_matching_cloud8)
    assert inv_not_matching_cloud8.total_sales == Decimal("215")
    assert inv_not_matching_cloud8.taxes_amount == Decimal("0.00")

    inv_no_tax_product = invoice.line_items.get(item=no_tax_product)
    assert inv_no_tax_product.total_sales == Decimal("5.00")
    assert inv_no_tax_product.taxes_amount == Decimal("0.00")

    inv_vape_juice = invoice.line_items.get(item=vape_juice)
    assert inv_vape_juice.total_sales == Decimal("10.00")
    assert inv_vape_juice.taxes_amount == Decimal("0.00")

    inv_otp_item = invoice.line_items.get(item=otp_item)
    assert inv_otp_item.total_sales == Decimal("18.00")
    assert inv_otp_item.taxes_amount == Decimal("0.00")


def test_il_taxes(
    invoice, disposable_vape, matching_cloud8, not_matching_cloud8, no_tax_product, vape_juice, otp_item
):
    invoice.invoice_level_tax_authority = "IL"
    invoice.save()
    taxes.extract_taxes(invoice)
    invoice.refresh_from_db()

    inv_disposable_vape = invoice.line_items.get(item=disposable_vape)
    assert inv_disposable_vape.total_sales == Decimal("189.29")
    assert inv_disposable_vape.taxes_amount == Decimal("25.71")

    inv_matching_cloud8 = invoice.line_items.get(item=matching_cloud8)
    assert inv_matching_cloud8.total_sales == Decimal("170.7345")
    assert inv_matching_cloud8.taxes_amount == Decimal("9.2655")

    inv_not_matching_cloud8 = invoice.line_items.get(item=not_matching_cloud8)
    assert inv_not_matching_cloud8.total_sales == Decimal("215")
    assert inv_not_matching_cloud8.taxes_amount == Decimal("0.00")

    inv_no_tax_product = invoice.line_items.get(item=no_tax_product)
    assert inv_no_tax_product.total_sales == Decimal("5.00")
    assert inv_no_tax_product.taxes_amount == Decimal("0.00")

    inv_vape_juice = invoice.line_items.get(item=vape_juice)
    assert inv_vape_juice.total_sales == Decimal("9.10")
    assert inv_vape_juice.taxes_amount == Decimal("0.90")

    inv_otp_item = invoice.line_items.get(item=otp_item)
    assert inv_otp_item.total_sales == Decimal("18.00")
    assert inv_otp_item.taxes_amount == Decimal("0.00")



