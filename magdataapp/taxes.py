# def determine_tax_amount(state, ounces=None, mls=None, items=None, amount=None):

#     if amount is None:
#         raise ValueError("Amount must be specified")

#     if ounces is None and mls is None and items is None:
#         raise ValueError("Must specify at least one of ounces, mls, items or amount")

#     return 0.00

import models


def extract_indiana_taxes(invoice):
    for line in invoice.line_items.select_related(
        "item"
    ).all():  # select_related tells the ORM to join against the Item
        category = line.item.category_name
        total = line.item_total
        price = line.item.purchase_price

        if line.item.otp_tax:
            # handle this here

        if category == "Disposable Vapes":
            line.item.total_sales = total / 1.15
            line.item.taxes_amount = total - (total / 1.15)
        elif category == "Cloud 8":
            matching_categories = [
                "1ML Cartridge",
                "1ML Disposable",
                "1ML Disposables",
                "2ML Disposables",
                "2ML Pro Dispostables",
            ]

            if line.item.reporting_sub_category in matching_categories:
                line.item.total_sales = total / 1.15
                line.item.taxes_amount = total - (total / 1.15)

        line.item.save()


def extract_taxes(invoice):

    ##INDIANA############################################################
    #####################################################################

    # IN Vape Tax == 15% of wholesale cost (purchase_price) for Closed Systems (Disposable Vapes and Cloud 8 Vapes)
    if invoice.invoice_level_tax_authority == "IN":
        extract_indiana_taxes(invoice)

    ##INDIANA############################################################

    ##KENTUCKY############################################################
    ######################################################################

    ## KY Vape Tax is $1.50 for each retail unit sold for disposable vapes (closed system) and Cloud 8 Vapes, and 15% of selling price (item_price) for Vape Juice (open system) items
    elif invoice.invoice_level_tax_authority == "KY":
        for line in invoice.line_items.select_related("item").all():
            if line.item.category_name == "Disposable Vapes":
                return line.item_total * 1.50 * line.item.retail_unit_in_wholesale
            elif line.item.category_name == "Vape Juice":
                return line.item_total / 1.15
            elif line.item.category_name == "Cloud 8":
                if line.item.reporting_sub_category == "1ML Cartridge":
                    return line.item_total * 1.50 * line.item.retail_unit_in_wholesale
                elif line.item.reporting_sub_category == "1ML Disposable":
                    return line.item_total * 1.50 * line.item.retail_unit_in_wholesale
                elif line.item.reporting_sub_category == "1ML Disposables":
                    return line.item_total * 1.50 * line.item.retail_unit_in_wholesale
                elif line.item.reporting_sub_category == "2ML Disposable":
                    return line.item_total * 1.50 * line.item.retail_unit_in_wholesale
                elif line.item.reporting_sub_category == "2ML Pro Disposable":
                    return line.item_total * 1.50 * line.item.retail_unit_in_wholesale
                else:
                    return line.item_total
            else:
                return line.item_total

    ##OHIO################################################################
    ######################################################################

    # OH vape tax == $.10 per ml
    elif invoice.invoice_level_tax_authority == "OH":
        for line in invoice.line_items.all():

            if line.item.category_name == "Disposable Vapes":
                return line.item_total - line.item.e_liquid_ml * line.quantity * 0.10
            elif line.item.category_name == "Vape Juice":
                return line.item_total - line.item.e_liquid_ml * line.quantity * 0.10
            elif line.item.category_name == "Cloud 8":
                if line.item.reporting_sub_category == "1ML Cartridge":
                    return (
                        line.item_total - line.item.e_liquid_ml * line.quantity * 0.10
                    )
                elif line.item.reporting_sub_category == "1ML Disposable":
                    return (
                        line.item_total - line.item.e_liquid_ml * line.quantity * 0.10
                    )
                elif line.item.reporting_sub_category == "1ML Disposables":
                    return (
                        line.item_total - line.item.e_liquid_ml * line.quantity * 0.10
                    )
                elif line.item.reporting_sub_category == "2ML Disposable":
                    return (
                        line.item_total - line.item.e_liquid_ml * line.quantity * 0.10
                    )
                elif line.item.reporting_sub_category == "2ML Pro Disposable":
                    return (
                        line.item_total - line.item.e_liquid_ml * line.quantity * 0.10
                    )
                else:
                    return line.item_total
            else:
                return line.item_total

    ##WEST VIRGINIA#######################################################
    ######################################################################

    # WV Vape Tax == $0.075 per ml
    elif invoice.invoice_level_tax_authority == "WV":
        for line in invoice.line_items.all():
            if line.item.category_name == "Disposable Vapes":
                return line.item_total - line.item.e_liquid_ml * line.quantity * 0.075
            elif line.item.category_name == "Vape Juice":
                return line.item_total - line.item.e_liquid_ml * line.quantity * 0.075
            elif line.item.category_name == "Cloud 8":
                if line.item.reporting_sub_category == "1ML Cartridge":
                    return (
                        line.item_total - line.item.e_liquid_ml * line.quantity * 0.075
                    )
                elif line.item.reporting_sub_category == "1ML Disposable":
                    return (
                        line.item_total - line.item.e_liquid_ml * line.quantity * 0.075
                    )
                elif line.item.reporting_sub_category == "1ML Disposables":
                    return (
                        line.item_total - line.item.e_liquid_ml * line.quantity * 0.075
                    )
                elif line.item.reporting_sub_category == "2ML Disposable":
                    return (
                        line.item_total - line.item.e_liquid_ml * line.quantity * 0.075
                    )
                elif line.item.reporting_sub_category == "2ML Pro Disposable":
                    return (
                        line.item_total - line.item.e_liquid_ml * line.quantity * 0.075
                    )
                else:
                    return line.item_total
            else:
                return line.item_total

    ##ILLINOIS############################################################
    ######################################################################

    # IL Vape Tax == 15% wholesale cost for open and closed systems
    elif invoice.invoice_level_tax_authority == "IL":
        for line in invoice.line_items.all():
            if line.item.category_name == "Disposable Vapes":
                return line.item_total - line.item.purchase_price * line.quantity * 0.15
            elif line.item.category_name == "Vape Juice":
                return line.item_total - line.item.purchase_price * line.quantity * 0.15
            elif line.category_name == "Cloud 8":
                if line.item.reporting_sub_category == "1ML Cartridge":
                    return (
                        line.item_total
                        - line.item.purchase_price * line.quantity * 0.15
                    )
                elif line.item.reporting_sub_category == "1ML Disposable":
                    return (
                        line.item_total
                        - line.item.purchase_price * line.quantity * 0.15
                    )
                elif line.item.reporting_sub_category == "1ML Disposables":
                    return (
                        line.item_total
                        - line.item.purchase_price * line.quantity * 0.15
                    )
                elif line.item.reporting_sub_category == "2ML Disposables":
                    return (
                        line.item_total
                        - line.item.purchase_price * line.quantity * 0.15
                    )
                elif line.item.reporting_sub_category == "2ML Pro Disposables":
                    return (
                        line.item_total
                        - line.item.purchase_price * line.quantity * 0.15
                    )
                else:
                    return line.item_total
            else:
                return line.item_total


    line.item.total_sales = line.item_total
    line.item.taxes_amount = 0.00
    line.item.save()
