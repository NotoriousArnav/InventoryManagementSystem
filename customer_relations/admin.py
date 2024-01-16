from django.contrib import admin
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from .models import *

#Dashboard View
class InvoiceItemView(admin.ModelAdmin):
    list_display = ('product', 'invoice', 'quantity', 'subtotal', 'invoice_id')

class InvoiceView(admin.ModelAdmin):
    list_display = ('customer', 'invoice_date', 'coupon', 'total_amount', 'final_amount', 'display_calculated_discount', 'id')

    def display_calculated_discount(self, obj):
        return round(obj.calculated_discount(), 2)  # Display with 2 decimal places

    display_calculated_discount.short_description = 'Calculated Discount'

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1

class CustomInvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceItemInline]

    list_display = ('customer', 'invoice_date', 'coupon', 'total_amount', 'final_amount', 'calculated_discount')
    actions = ['export_to_pdf']

    
    def export_to_pdf(modeladmin, request, queryset):
    # Create a PDF document
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="invoices.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

    # Loop through each selected invoice and add its data to the PDF
        for invoice in queryset:
            data = []
            data.append(["Invoice ID", str(invoice.id)])
            data.append(["Customer", str(invoice.customer.user.first_name+' '+invoice.customer.user.last_name)])
            data.append(["Customer Phone", str(invoice.customer.phone_number)])
            data.append(["Invoice Date", str(invoice.invoice_date)])
            data.append(["Total Amount", str(invoice.total_amount())])
            data.append(["Discounted Amount", str(invoice.final_amount())])

        # Add more fields as needed

        # Add a header row for Invoice Items
        data.append(["Product", "Quantity", "Subtotal"])

        # Add rows for each InvoiceItem
        for item in invoice.invoiceitem_set.all():
            data.append([item.product.name, item.quantity, item.subtotal()])

        # Create a Table object
        table = Table(data)

        # Apply style to the table
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), '#77a7c2'),
                            ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), '#f5f5f5'),
                            ('GRID', (0, 0), (-1, -1), 1, '#a5a5a5')])

        table.setStyle(style)

        elements.append(table)
        elements.append(canvas.Canvas(response).showPage())  # Start a new page for each invoice

        doc.build(elements)

        return response

    export_to_pdf.short_description = "Export selected invoices to PDF"

# Register the models and the custom admin class
admin.site.register(Invoice, CustomInvoiceAdmin)

# Register your models here.
admin.site.register(Customer)
admin.site.register(Coupon)
#admin.site.register(Invoice, InvoiceView)
admin.site.register(InvoiceItem, InvoiceItemView)
