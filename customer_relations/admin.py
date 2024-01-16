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
    readonly_fields = ['subtotal']

class CustomInvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceItemInline]

    list_display = ('customer', 'invoice_date', 'coupon', 'total_amount', 'final_amount', 'calculated_discount', 'transaction_status')
    actions = ['export_to_pdf']

    def export_to_pdf(modeladmin, request, queryset):
    # Create a PDF document
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="invoices.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

    # Loop through each selected invoice and add its data to the PDF
        for invoice in queryset:
        # Table for Invoice Header
            header_data = [
                ["Invoice ID", str(invoice.id)],
                ["Customer", str(invoice.customer.user.first_name + ' ' + invoice.customer.user.last_name)],
                ["Customer Phone", str(invoice.customer.phone_number)],
                ["Invoice Date", str(invoice.invoice_date)],
                ["Total Amount", str(invoice.total_amount())],
                ["Discounted Amount", str(invoice.final_amount())],
            ]

            header_table = Table(header_data, colWidths='100%')
            header_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), '#77a7c2'),
                ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), '#f5f5f5'),
                ('GRID', (0, 0), (-1, -1), 1, '#a5a5a5')
            ])
            header_table.setStyle(header_style)

        # Table for Invoice Items
            item_data = [
                ["Product", "Quantity", "Subtotal"]
            ]
            for item in invoice.invoiceitem_set.all():
                item_data.append([item.product.name, item.quantity, item.subtotal()])

            item_table = Table(item_data, colWidths='100%')
            item_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), '#77a7c2'),
                ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), '#f5f5f5'),
                ('GRID', (0, 0), (-1, -1), 1, '#a5a5a5')
            ])
            item_table.setStyle(item_style)

        # Add both tables to the elements list
            elements.append(header_table)
            elements.append(item_table)
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
