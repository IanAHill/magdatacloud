from django.contrib import admin

from .models import Customer, Item, Invoice, Invoice_Line_Item


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display = ("customer_name", "customer_sub_type", "customer_pays_vape_tax")
    list_filter = ("customer_sub_type", "customer_pays_vape_tax")
    search_fields = ("customer_name", "customer", "business_ein")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    model = Item
    list_display = ("item_name", "product", "sku", "stock_on_hand")


class LineItemInline(admin.StackedInline):
    model = Invoice_Line_Item
    extra = 0


@admin.register(Invoice)
class Invoice(admin.ModelAdmin):
    model = Invoice
    date_hierarchy = "invoice_date"
    inlines = [LineItemInline]
    list_display = (
        "invoice_number",
        "invoice",
        "customer",
        "invoice_date",
        "invoice_status",
    )
