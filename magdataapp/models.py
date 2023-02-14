from django.db import models
from django_extensions.db.models import TimeStampedModel

#############################################################################################################
## Model for Customer #######################################################################################
#############################################################################################################

class Customer(TimeStampedModel):
   created_time = models.DateTimeField(editable=False)
   customer_id = models.PositiveBigIntegerField() ## the contact ID from Zoho
   TYPE_CHOICES = [
      ("BUSINESS", "Business"),
      ("INDIVIDUAL", "Individual"),
   ]
   customer_sub_type = models.CharField(max_lenth=2, choices=TYPE_CHOICES, default="BUSINESS")
   taxable = models.BooleanField(default=True)
   tax_authority = models.CharField(max_length=2) ## needs to be all capital 2-digit state code
   customer_name = models.CharField()
   shipping_address = models.CharField()
   shipping_address_line_2 = models.CharField()
   shipping_city = models.CharField()
   shipping_state = models.CharField()
   shipping_code = models.PositiveSmallIntegerField(max_length=5)  ## what to do about the few that have the extra numbers on the end?
   assigned_sales_person = models.CharField()
   state_manager = models.CharField()
   business_ein = models.CharField()
   tobacco_license = models.CharField()
   parent_chain = models.CharField()
   CUSTOMER_TYPE_CHOICES = [
      ("CHAIN", "Chain"),
      ("CONSUMER", "Consumer"),
      ("DISTRIBUTOR", "Distributor"),
      ("INDEPENDENT_STORE", "Independent Store"),
   ]
   customer_type = models.CharField(choices=CUSTOMER_TYPE_CHOICES, null=True, default="")
   customer_pays_vape_tax = models.BooleanField(null=True) ## can be true or false or blank, because it doesn't apply to every state

#############################################################################################################
#############################################################################################################




#############################################################################################################
## Model for Items ##########################################################################################
#############################################################################################################

class Item(TimeStampedModel):
   product_id = models.PositiveBigIntegerField()  ## id field from zoho
   sku = models.CharField(unique=True)
   purchase_price = models.DecimalField()
   preferred_vendor = models.CharField() ##another example of something with tons of choices
   stock_on_hand = models.PositiveSmallIntegerField()
   category_name = models.CharField() ##choices
   e_liquid_ml = models.FloatField()
   msrp = models.DecimalField()
   reporting_category_primary = models.CharField()  ##choices
   reporting_category_secondary = models.CharField() ##choices
   reporting_category_cannabinoid = models.CharField() ##choices
   cloud8_b2c = models.BooleanField()
   b2c_msrp = models.DecimalField()

#############################################################################################################
#############################################################################################################




#############################################################################################################
## Model for Invoices  ######################################################################################
#############################################################################################################

class Invoice(TimeStampedModel):
   invoice_id = models.PositiveBigIntegerField() ## The unique ID for invoices in Zoho, separate from the invoice number for some reason. I don't use this, so since invoices will have their own Django assigned unique ID, maybe we don't need this?
   customer = models.ForeignKey("Customer", on_delete=models.PROTECT) 
   invoice_number = models.CharField() 
   invoice_level_tax_authority = models.CharField() ## state code choices, could inherit from attached Customer
   invoice_date = models.DateField()
   invoice_status = models.CharField() ##needs to have invoice_status choices

#############################################################################################################
#############################################################################################################







#############################################################################################################
## Model for Invoice Line Items  ############################################################################
#############################################################################################################

class Invoice_Line_Item(TimeStampedModel):
   invoice_id = models.ForeignKey("Invoice", on_delete=models.CASCADE)
   product_id = models.ForeignKey("Item")

   quantity = models.PositiveIntegerField()
   item_price = models.DecimalField()
   item_total = models.DecimalField()

   ## will this class have access to properties of Customer? since it is a foreign key of a foreign key? customer->invoice->invoice_line_item

#############################################################################################################
#############################################################################################################




#############################################################################################################
## Model for Taxes  #########################################################################################
#############################################################################################################

class Taxes(TimeStampedModel):
   pa_otp_tax_number_of_ounces = models.FloatField() 
   pa_otp_tax_per_item = models.FloatField()
   oh_otp_tax_per_item = models.FloatField()
   wv_otp_tax_per_item = models.FloatField()
   pa_vape_tax_rate = models.PositiveSmallIntegerField() ##### can be 40 or nothing... is there an easy way to define the choices in the parameters without having to create separate variables?
   oh_vape_tax_per_ml = models.FloatField()
   oh_vape_tax_per_item = models.FloatField()
   wv_vape_tax_per_item = models.FloatField()
   ky_vape_tax_per_item = models.PositiveSmallIntegerField() ###### can be 15 or nothing.
   in_vape_tax_rate = models.PositiveSmallIntegerField() ###### can be 15% or nothing
   il_vape_tax_per_item = models.FloatField()
   va_vape_tax_per_item = models.FloatField()
   nc_vape_tax_per_item = models.FloatField()
   de_vape_tax_per_item = models.FloatField()

#### Add Price List Class
