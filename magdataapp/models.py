from django.db import models

#############################################################################################################
## Model for Customer ("Contact" table in Zoho) #############################################################
#############################################################################################################

class Contact(models.Model):
   created_time = models.DateTimeField(editable=False)
   contact_id = models.PositiveBigIntegerField() ## the contact ID from Zoho
   
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

   contact_name = models.CharField()
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



















