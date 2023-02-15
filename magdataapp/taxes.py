def determine_tax_amount(state, ounces=None, mls=None, items=None, amount=None):

    if amount is None:
        raise ValueError("Amount must be specified")

    if ounces is None and mls is None and items is None:
        raise ValueError("Must specify at least one of ounces, mls, items or amount")

    return 0.00
