import pytest

from magdatapp.models import *

def test_pytest():
    # Just to make sure pytest is up and working
    assert True


def test_invalid_arguments():

    with pytest.raises(ValueError):
        determine_tax_amount(state="PA")

# Equivalient to the above pytest.raises
#    failed = False
#    try:
#        determine_tax_amount(state="PA")
#    except ValueError:
#        failed = True
#
#    assert failed

    with pytest.raises(ValueError):
        determine_tax_amount(state="PA", ounces=3)


def test_valid_arguments():
    assert determine_tax_amount(state="PA", ounces=3, amount=10.01) == 0.00


def test_in_taxes(db):
    i = Invoice.objects.create(....)
    l1 = LineItem.objects.create(....)
    l2 = LineItem.objects.create(....)
    l3 = LineItem.objects.create(....)
    l4 = LineItem.objects.create(....)

    extract_taxes(i)

    i.refresh_from_db()
    l1.refresh_from_db()
    l2.refresh_from_db()
    l3.refresh_from_db()
    l4.refresh_from_db()

    assert i.total_tax == 0.00
    assert l1.taxes_amount == 0.00
    assert l2.taxes_amount == 0.00
    assert l3.taxes_amount == 0.00
    assert l4.taxes_amount == 0.00