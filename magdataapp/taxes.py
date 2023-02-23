import models

def extract_IN_taxes(invoice):
    for line in invoice.line_items.select_related("item").all():  # select_related tells the ORM to join against the Item
        category = line.item.category_name
        total = line.item_total
        price = line.item.purchase_price
        qty = line.quantity
        # IN Vape Tax == 15% of wholesale cost on closed systems only
        if category == "Disposable Vapes":
            line.item.total_sales = total - price * qty * 0.15
            line.item.taxes_amount = price * qty * 0.15
        elif category == "Cloud 8":
            matching_categories = [
                "1ML Cartridge",
                "1ML Disposable",
                "1ML Disposables",
                "2ML Disposables",
                "2ML Pro Dispostables",
            ]
            if line.item.reporting_sub_category in matching_categories:
                line.item.total_sales = total - price * qty * 0.15
                line.item.taxes_amount = price * qty * 0.15

        line.item.save()



def extract_KY_taxes(invoice):
    for line in invoice.line_items.select_related("item").all():
        category = line.item.category_name
        total = line.item_total
        qty = line.quantity
        units = line.item.retail_unit_in_wholesale

        #vape tax for open systems
        if category == "Vape Juice":
            line.item.total_sales = total / 1.15
            line.item.taxes_amount = (total / 1.15) * .15
        #vape tax for closed systems
        elif category == "Disposable Vapes":
            line.item.total_sales = total * 1.50 * units    
            line.item.taxes_amount = 1.50 * units 
        elif category == "Cloud 8":
            matching_categories = [
                "1ML Cartridge",
                "1ML Disposable",
                "1ML Disposables",
                "2ML Disposables",
                "2ML Pro Dispostables",
            ]
            if line.item.reporting_sub_category in matching_categories:
                line.item.total_sales = total * 1.50 * units
                line.item.taxes_amount = 1.50 * units
        
        line.item.save()
  


def extract_OH_taxes(invoice):
    for line in invoice.line_items.select_related("item").all():
        category = line.item.category_name
        total = line.item_total
        qty = line.quantity
        mls = line.item.e_liquid_ml
        #OTP Tax
        if line.item.otp_tax:
            line.item.total_sales = total - line.item.OH_otp_tax * qty
            line.item.taxes_amount = line.item.OH_otp_tax * qty
        #Vape Tax == .10 * mls for open and closed systems
        if category == "Disposable Vapes":
            line.item.total_sales = total - (mls * qty * 0.10)
            line.item.taxes_amount = mls * qty * 0.10
        elif category == "Vape Juice":
            line.item.total_sales = total - (mls * qty * 0.10)
            line.item.taxes_amount = mls * qty * 0.10
        elif category == "Cloud 8":
            matching_categories = [
                "1ML Cartridge",
                "1ML Disposable",
                "1ML Disposables",
                "2ML Disposables",
                "2ML Pro Dispostables",
            ]
            if line.item.reporting_sub_category in matching_categories:
                line.item.total_sales = total - (mls * qty * 0.10)
                line.item.taxes_amount = mls * qty * 0.10
        
        line.item.save()
                


def extract_WV_taxes(invoice):
    for line in invoice.line_items.select_related("item").all():
        category = line.item.category_name
        total = line.item_total
        qty = line.quantity
        mls = line.item.e_liquid_ml
        #OTP Tax
        if line.item.WV_otp_tax:
            line.item.total_sales = total - line.item.WV_otp_tax * qty
            line.item.taxes_amount = line.item.WV_otp_tax * qty
        #Vape Tax == $0.075 per ml
        if category == "Disposable Vapes":
            line.item.total_sales = total - (mls * qty * 0.075)
            line.item.taxes_amount = mls * qty * 0.075
        elif category == "Vape Juice":
            line.item.total_sales = total - (mls * qty * 0.075)
            line.item.taxes_amount = mls * qty * 0.075
        elif category == "Cloud 8":
            matching_categories = [
                "1ML Cartridge",
                "1ML Disposable",
                "1ML Disposables",
                "2ML Disposables",
                "2ML Pro Dispostables",
            ]
            if line.item.reporting_sub_category in matching_categories:
                line.item.total_sales = total - (mls * qty * 0.075)
                line.item.taxes_amount = mls * qty * 0.075
        
        line.item.save()



def extract_IL_taxes(invoice):
    for line in invoice.line_items.select_related("item").all():
        price = line.item.purchase_price
        category = line.item.category_name
        total = line.item_total
        qty = line.quantity    
        # IL Vape Tax == 15% wholesale cost for open and closed systems
        if category == "Disposable Vapes":
            line.item.total_sales = total - (price * qty * 0.15)
            line.item.taxes_amount = price * qty * 0.15
        elif category == "Vape Juice":
            line.item.total_sales = total - (price * qty * 0.15)
            line.item.taxes_amount = price * qty * 0.15
        elif category == "Cloud 8":
            matching_categories = [
                "1ML Cartridge",
                "1ML Disposable",
                "1ML Disposables",
                "2ML Disposables",
                "2ML Pro Dispostables",
            ]
            if line.item.reporting_sub_category in matching_categories:
                line.item.total_sales = total - (price * qty * 0.15)
                line.item.taxes_amount = price * qty * 0.15
        
        line.item.save()



def extract_PA_taxes(invoice):
    for line in invoice.line_items.select_related("item").all():
        total = line.item_total
        qty = line.quantity    
        if line.item.WV_otp_tax and not invoice.customer.customer_pays_vape_tax:
            line.item.total_sales = total - line.item.PA_otp_tax * qty
            line.item.taxes_amount = line.item.PA_otp_tax * qty

        line.item.save()


def extract_taxes(invoice):
    if invoice.invoice_level_tax_authority == "IN":
        extract_IN_taxes(invoice)
    elif invoice.invoice_level_tax_authority == "KY":
        extract_KY_taxes(invoice)
    elif invoice.invoice_level_tax_authority == "OH":
        extract_KY_taxes(invoice)
    elif invoice.invoice_level_tax_authority == "WV":
        extract_KY_taxes(invoice)
    elif invoice.invoice_level_tax_authority == "IL":
        extract_KY_taxes(invoice)
    elif invoice.invoice_level_tax_authority == "PA":
        extract_PA_taxes(invoice)
    else:
        for line in invoice.line_items.select_related("item").all():
            line.item.total_sales = line.item_total
            line.item.taxes_amount = 0.00
        line.item.save()
