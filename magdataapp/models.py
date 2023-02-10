from django.db import models

## Where is the best place to set global variables, like state choices?


#############################################################################################################
## Model for Customer #######################################################################################
#############################################################################################################

class Customer(models.Model):
   created_time = models.DateTimeField(editable=False)
   customer_id = models.PositiveBigIntegerField() ## the contact ID from Zoho
   
   ######### Customer Type *************
   ## contact_type exists as a field in Zoho, but it only has one option, customer. Could there be future use for this?
   BUSINESS = "BU"
   INDIVIDUAL = "IN"
   SUB_TYPE_CHOICES = [
      (BUSINESS, "Business"),
      (INDIVIDUAL, "Individual"),
   ]
   customer_sub_type = models.CharField(max_lenth=2, choices=SUB_TYPE_CHOICES, default=BUSINESS)



   ######### Tax Info #######################################################
   PA_OTP_TAX = "PAOTP"
   WISCONSIN_SALES_TAX = "WI"
   TAX_NAME_CHOICES = [
      (PA_OTP_TAX, "PA OTP tax"),
      (WISCONSIN_SALES_TAX, "Wisconsin - Sales Tax"),
   ]
   TAX_PERCENTAGE_CHOICES = [
      (40, "40"),
      (5, "5"),
   ]
   taxable = models.BooleanField(default=True)
   tax_name = models.CharField(choices=TAX_NAME_CHOICES, null=True, default="")
   tax_percentage = models.SmallIntegerField(max_length=3, choices=TAX_PERCENTAGE_CHOICES, null=True)
   ##tax_type
   ##exemption_reason
   ##tax_authority --- needs to be one of 50 states. 50 choices?
   #############################################################################

   customer_name = models.CharField()
   ##price_list = models.CharField()   ---- This is really important, and has like 30 choices. Not sure the best way to implement. 
   ##payment_terms = models.SmallIntegerField()  --- Also really important, but not for my purposes... not sure what to include and what not to...
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

class Item(models.Model):
   product_id = models.PositiveBigIntegerField()  ## id field from zoho
   ##brand -- not very useful for my purposes, also, has like 50 options
   ##manufacturer -- same
   sku = models.CharField(unique=True)
   purchase_price = models.FloatField()
   preferred_vendor = models.CharField() ##another example of something with tons of choices
   stock_on_hand = models.PositiveSmallIntegerField()
   category_name = models.CharField() ##choices
   e_liquid_ml = models.FloatField()
   sub_category = models.CharField() #choices

   pa_otp_tax_number_of_ounces = models.FloatField() #important for cacluating tax reports
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

   msrp = models.FloatField()

   reporting_category_primary = models.CharField()  ##choices
   reporting_category_secondary = models.CharField() ##choices
   reporting_category_cannabinoid = models.CharField() ##choices
   cloud8_b2c = models.BooleanField()
   b2c_msrp = models.FloatField()

#############################################################################################################
#############################################################################################################




#############################################################################################################
## Model for Invoices  ######################################################################################
#############################################################################################################

class Invoice(models.Model):
   invoice_id = models.PositiveBigIntegerField() ## The unique ID for invoices in Zoho, separate from the invoice number for some reason. I don't use this, so since invoices will have their own Django assigned unique ID, maybe we don't need this?
   customer_id = models.ForeignKey("Customer") ### I think I do NOT want the invoice to delete (cascade) if the customer is deleted??
   invoice_number = models.CharField() ##they increment automatically in Zoho, but not just a number (i.e. INV-02016). won't be the primary key for this database.
   invoice_level_tax_authority = models.CharField() ## state code choices
   invoice_date = models.DateField()
   invoice_status = models.CharField() ##needs to have invoice_status choices

#############################################################################################################
#############################################################################################################




#############################################################################################################
## Model for Invoice Line Items  ############################################################################
#############################################################################################################

class Invoice_Line_Item(models.Model):
   invoice_id = models.ForeignKey("Invoice", on_delete=models.CASCADE)
   product_id = models.ForeignKey("Item")

   quantity = models.PositiveIntegerField()
   item_price = models.FloatField()
   item_total = models.FloatField()

   ## will this class have access to properties of Customer? since it is a foreign key of a foreign key? customer->invoice->invoice_line_item


