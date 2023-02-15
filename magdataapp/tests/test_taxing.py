from magdataapp.taxes import determine_tax_amount
import pytest


def test_pytest():
    # Just to make sure pytest is up and working
    assert True


def test_invalid_arguments():

    with pytest.raises(ValueError):
        determine_tax_amount(state="PA")

    with pytest.raises(ValueError):
        determine_tax_amount(state="PA", ounces=3)


def test_valid_arguments():
    assert determine_tax_amount(state="PA", ounces=3, amount=10.01) == 0.00
