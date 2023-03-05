from decimal import Decimal

MATCHING_CATEGORIES = [
    "1ML Cartridge",
    "1ML Disposable",
    "1ML Disposables",
    "2ML Disposables",
    "2ML Pro Disposables",
]


def extract_IN_taxes(invoice):
    for line in invoice.line_items.select_related(
        "item"
    ).all():  # select_related tells the ORM to join against the Item
        category = line.item.category_name
        total = line.item_total
        price = line.item.purchase_price
        qty = line.quantity
        # IN Vape Tax == 15% of wholesale cost on closed systems only
        if category == "Disposable Vapes":
            line.total_sales = total - price * qty * Decimal(0.15)
            line.taxes_amount = price * qty * Decimal(0.15)
        elif category == "Cloud 8":
            if line.item.reporting_sub_category in MATCHING_CATEGORIES:
                line.total_sales = total - price * qty * Decimal(0.15)
                line.taxes_amount = price * qty * Decimal(0.15)
        else:
            line.total_sales = total
            line.taxes_amount = 0.00
        line.save()


def extract_KY_taxes(invoice):
    for line in invoice.line_items.select_related("item").all():
        category = line.item.category_name
        total = line.item_total
        qty = line.quantity
        units = line.item.retail_units_in_wholesale

        # vape tax for open systems
        if category == "Vape Juice":
            line.total_sales = total / Decimal(1.15)
            line.taxes_amount = (total / Decimal(1.15)) * Decimal(0.15)
        # vape tax for closed systems
        elif category == "Disposable Vapes":
            line.total_sales = total - qty * Decimal(1.50) * units
            line.taxes_amount = Decimal(1.50) * units * qty
        elif category == "Cloud 8":
            if line.item.reporting_sub_category in MATCHING_CATEGORIES:
                line.total_sales = total - (Decimal(1.50) * units * qty)
                line.taxes_amount = Decimal(1.50) * units * qty
            else:
                line.total_sales = total
                line.taxes_amount = 0.00
        else:
            line.total_sales = total
            line.taxes_amount = 0.00
        line.save()


def extract_OH_taxes(invoice):
    for line in invoice.line_items.select_related("item").all():
        category = line.item.category_name
        total = line.item_total
        qty = line.quantity
        mls = Decimal(line.item.e_liquid_ml)
        # OTP Tax
        if line.item.OH_otp_tax:
            line.total_sales = total - line.item.OH_otp_tax * qty
            line.taxes_amount = line.item.OH_otp_tax * qty
        # Vape Tax == .10 * mls for open and closed systems, not cloud 8 products (nicotene only)
        if category == "Disposable Vapes":
            line.total_sales = total - (mls * qty * Decimal(0.10))
            line.taxes_amount = mls * qty * Decimal(0.10)
        elif category == "Vape Juice":
            line.total_sales = total - (mls * qty * Decimal(0.10))
            line.taxes_amount = mls * qty * Decimal(0.10)
        else:
            line.total_sales = total
            line.taxes_amount = 0.00
        line.save()


def extract_WV_taxes(invoice):
    for line in invoice.line_items.select_related("item").all():
        category = line.item.category_name
        total = line.item_total
        qty = line.quantity
        mls = line.item.e_liquid_ml
        # OTP Tax
        if line.item.WV_otp_tax:
            line.total_sales = total - line.item.WV_otp_tax * qty
            line.taxes_amount = line.item.WV_otp_tax * qty
        # Vape Tax == $0.075 per ml
        if category == "Disposable Vapes":
            line.total_sales = total - Decimal(mls * qty * 0.075)
            line.taxes_amount = mls * qty * 0.075
        elif category == "Vape Juice":
            line.total_sales = total - Decimal(mls * qty * 0.075)
            line.taxes_amount = mls * qty * 0.075
        elif category == "Cloud 8":
            if line.item.reporting_sub_category in MATCHING_CATEGORIES:
                line.total_sales = total - Decimal(mls * qty * 0.075)
                line.taxes_amount = mls * qty * 0.075
            else:
                line.total_sales = total
                line.taxes_amount = 0.00
        else:
            line.total_sales = total
            line.taxes_amount = 0.00
        line.save()


## NJ not needed, because non-nicotene vapes are not subject to vape tax in NJ, and we only sell Cloud 8 there because flavored nicotene vapes are banned in NJ.
# def extract_NJ_taxes(invoice):
#     for line in invoice.line_items.select_related("item").all():
#         category = line.item.category_name
#         total = line.item_total
#         qty = line.quantity
#         mls = line.item.e_liquid_ml

#         #NJ Vape Tax == $0.10 per ml for closed
#         if category == "Disposable Vapes":
#             line.item.total_sales = total - (mls * qty * 0.10)
#             line.item.taxes_amount = mls * qty * 0.10
#         elif category == "Cloud 8":
#             matching_categories = [
#                 "1ML Cartridge",
#                 "1ML Disposable",
#                 "1ML Disposables",
#                 "2ML Disposables",
#                 "2ML Pro Dispostables",
#             ]
#             if line.item.reporting_sub_category in matching_categories:
#                 line.item.total_sales = total - (mls * qty * 0.10)
#                 line.item.taxes_amount = mls * qty * 0.10

#         line.item.save()


def extract_IL_taxes(invoice):
    for line in invoice.line_items.select_related("item").all():
        price = line.item.purchase_price
        category = line.item.category_name
        total = line.item_total
        qty = line.quantity
        # IL Vape Tax == 15% wholesale cost for open and closed systems
        if category == "Disposable Vapes":
            line.total_sales = total - (price * qty * Decimal(0.15))
            line.taxes_amount = price * qty * Decimal(0.15)
        elif category == "Vape Juice":
            line.total_sales = total - (price * qty * Decimal(0.15))
            line.taxes_amount = price * qty * Decimal(0.15)
        elif category == "Cloud 8":
            if line.item.reporting_sub_category in MATCHING_CATEGORIES:
                line.total_sales = total - (price * qty * Decimal(0.15))
                line.taxes_amount = price * qty * Decimal(0.15)
        else:
            line.total_sales = total
            line.taxes_amount = 0.00
        line.save()


# zoho automatically extracts vape tax for PA
def extract_PA_taxes(invoice):
    for line in invoice.line_items.select_related("item").all():
        total = line.item_total
        qty = line.quantity
        if line.item.PA_otp_tax:
            line.total_sales = total - line.item.PA_otp_tax * qty
            line.taxes_amount = line.item.PA_otp_tax * qty
        else:
            line.total_sales = total
            line.taxes_amount = 0.00
        line.save()


def extract_taxes(invoice):
    if invoice.invoice_level_tax_authority == "IN":
        extract_IN_taxes(invoice)
    elif invoice.invoice_level_tax_authority == "KY":
        extract_KY_taxes(invoice)
    elif invoice.invoice_level_tax_authority == "OH":
        extract_OH_taxes(invoice)
    elif invoice.invoice_level_tax_authority == "WV":
        extract_WV_taxes(invoice)
    elif invoice.invoice_level_tax_authority == "IL":
        extract_IL_taxes(invoice)
    elif (
        invoice.invoice_level_tax_authority == "PA"
        and invoice.customer.taxable
        and not invoice.customer.customer_pays_vape_tax
    ):
        extract_PA_taxes(invoice)
        #### IF THE LOGIC ON LINE 187 FAILS, WE STILL NEED TO ASSIGN TOTAL_SALES AND TAXES_AMOUNT!!
    else:
        for line in invoice.line_items.select_related("item").all():
            line.total_sales = line.item_total
            line.taxes_amount = 0.00
            line.save()
