from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.utils import timezone

#############################################################################################################
## Model for Customer #######################################################################################
#############################################################################################################


class Customer(TimeStampedModel):
    created_time = models.DateTimeField(editable=False, default=timezone.now())
    customer = models.PositiveBigIntegerField()  ## the contact ID from Zoho
    TYPE_CHOICES = [
        ("BUSINESS", "Business"),
        ("INDIVIDUAL", "Individual"),
    ]
    customer_sub_type = models.CharField(
        max_length=30, choices=TYPE_CHOICES, default="BUSINESS"
    )
    taxable = models.BooleanField(default=True)
    customer_name = models.CharField(max_length=30)
    shipping_address = models.CharField(max_length=30)
    shipping_address_line_2 = models.CharField(max_length=30, null=True, blank=True)
    shipping_city = models.CharField(max_length=30)
    shipping_state = models.CharField(max_length=30)
    shipping_code = models.PositiveSmallIntegerField()
    assigned_sales_person = models.CharField(max_length=30)
    state_manager = models.CharField(max_length=30)
    business_ein = models.CharField(max_length=30)
    tobacco_license = models.CharField(max_length=30)
    parent_chain = models.CharField(max_length=30, null=True, blank=True)
    CUSTOMER_TYPE_CHOICES = [
        ("CHAIN", "Chain"),
        ("CONSUMER", "Consumer"),
        ("DISTRIBUTOR", "Distributor"),
        ("INDEPENDENT_STORE", "Independent Store"),
    ]
    customer_type = models.CharField(
        max_length=30, choices=CUSTOMER_TYPE_CHOICES, null=True, default=""
    )
    customer_pays_vape_tax = models.BooleanField(null=True)

    def __str__(self):
        return self.customer_name


#############################################################################################################
## Model for Items ##########################################################################################
#############################################################################################################


class Item(TimeStampedModel):
    product = models.PositiveBigIntegerField()  ## id field from zoho
    sku = models.CharField(max_length=30, unique=True)
    item_name = models.CharField(max_length=100)
    purchase_price = models.DecimalField(decimal_places=2, max_digits=7)
    preferred_vendor = models.CharField(
        max_length=30
    )  ##another example of something with tons of choices
    stock_on_hand = models.PositiveSmallIntegerField()
    category_name = models.CharField(max_length=30)  ##choices
    e_liquid_ml = models.FloatField()
    msrp = models.DecimalField(decimal_places=2, max_digits=7)
    reporting_sub_category = models.CharField(max_length=30)
    reporting_category_primary = models.CharField(max_length=30)  ##choices
    reporting_category_cannabinoid = models.CharField(max_length=30)  ##choices
    cloud8_b2c = models.BooleanField()
    b2c_msrp = models.DecimalField(decimal_places=2, max_digits=7, null=True)
    retail_units_in_wholesale = models.PositiveSmallIntegerField()
    OH_otp_tax = models.DecimalField(
        decimal_places=2, max_digits=7, blank=True, null=True
    )
    PA_otp_tax = models.DecimalField(
        decimal_places=2, max_digits=7, blank=True, null=True
    )
    WV_otp_tax = models.DecimalField(
        decimal_places=2, max_digits=7, blank=True, null=True
    )

    def __str__(self):
        return self.item_name


#############################################################################################################
## Model for Invoices  ######################################################################################
#############################################################################################################


class Invoice(TimeStampedModel):
    invoice = models.PositiveBigIntegerField()
    customer = models.ForeignKey("Customer", on_delete=models.PROTECT)
    invoice_number = models.CharField(max_length=30)
    invoice_level_tax_authority = models.CharField(max_length=30)
    invoice_date = models.DateField()
    invoice_status = models.CharField(max_length=30)

    def __str__(self):
        return f"Invoice #{self.invoice_number}"


#############################################################################################################
## Model for Invoice Line Items  ############################################################################
#############################################################################################################


class Invoice_Line_Item(TimeStampedModel):
    invoice = models.ForeignKey(
        "Invoice", on_delete=models.CASCADE, related_name="line_items"
    )
    item = models.ForeignKey(
        "Item", on_delete=models.CASCADE, related_name="line_items"
    )

    quantity = models.PositiveIntegerField()
    item_price = models.DecimalField(decimal_places=2, max_digits=7)
    item_total = models.FloatField()
    taxes_amount = models.DecimalField(decimal_places=2, max_digits=7)
    total_sales = models.DecimalField(
        decimal_places=2, max_digits=7, default=0.00
    )  ##add to other decimal fields for testing purposes
