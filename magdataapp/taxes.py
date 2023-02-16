# def determine_tax_amount(state, ounces=None, mls=None, items=None, amount=None):

#     if amount is None:
#         raise ValueError("Amount must be specified")

#     if ounces is None and mls is None and items is None:
#         raise ValueError("Must specify at least one of ounces, mls, items or amount")

#     return 0.00

import models

def extract_taxes(invoice): ## should the paramenter be invoice, in which case it will execute tax extraction on each line item belonging to the invoice, or just take invoice_line_item as an argument?
    
    ##INDIANA has an easy tax, 15% of total sale off any of the items with category "Disposable Vapes", or Cloud 8 Products with the listed sub_categories.
    if invoice.invoice_level_tax_authority == "IN":
        if item.category_name == "Disposable Vapes":
            return invoice_line_item.item_total/1.15 ##should return a new item total that has the 15% tax removed. How to put the extracted tax amount into a separate field?
        elif item.category_name == "Cloud 8":
            if item.reporting_sub_category == "1ML Cartridge":
                return invoice_line_item.item_total/1.15
            elif item.reporting_sub_category == "1ML Disposable":
                return invoice_line_item.item_total/1.15
            elif item.reporting_sub_category == "1ML Disposables": ## this is stupid, because it should be the same as 1ML Disposable case as above, but people just enter some items wrong.
                return invoice_line_item.item_total/1.15
            elif item.reporting_sub_category == "2ML Disposable":
                return invoice_line_item.item_total/1.15
            elif item.reporting_sub_category == "2ML Pro Disposable":
                return invoice_line_item.item_total/1.15
            else:
                return invoice_line_item.item_total ##all other cloud 8 products are not subject to this tax
        else:
            return invoice_line_item.item_total/1.15
        

    ## KY Vape Tax is $1.50 for every single retail unit sold for disposable vapes (closed system) and certain cloud 8 products, and 15% for Vape Juice (open system) items
    elif invoice.invoice_level_tax_authority == "KY":
        if item.category_name == "Disposable Vapes":
            return invoice_line_item.item_total*1.50*item.retail_until_in_wholesale
        elif item.category_name == "Vape Juice":
            return invoice_line_item.item_total/1.15
        elif item.category_name == "Cloud 8":
            if item.reporting_sub_category == "1ML Cartridge":
                return invoice_line_item.item_total*1.50*item.retail_until_in_wholesale
            elif item.reporting_sub_category == "1ML Disposable":
                return invoice_line_item.item_total*1.50*item.retail_until_in_wholesale
            elif item.reporting_sub_category == "1ML Disposables": ## this is stupid, because it should be the same as 1ML Disposable case as above, but people just enter some items wrong.
                return invoice_line_item.item_total*1.50*item.retail_until_in_wholesale
            elif item.reporting_sub_category == "2ML Disposable":
                return invoice_line_item.item_total*1.50*item.retail_until_in_wholesale
            elif item.reporting_sub_category == "2ML Pro Disposable":
                return invoice_line_item.item_total*1.50*item.retail_until_in_wholesale
            else:
                return invoice_line_item.item_total
        else:
            return invoice_line_item.item_total
