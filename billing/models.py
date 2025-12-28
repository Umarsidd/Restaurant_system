from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from decimal import Decimal
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.core.files.base import ContentFile


class Bill(models.Model):
    """Bill model for table payments"""
    
    class Status(models.TextChoices):
        NOT_GENERATED = 'NOT_GENERATED', 'Not Generated'
        PENDING_PAYMENT = 'PENDING_PAYMENT', 'Pending Payment'
        PAID = 'PAID', 'Paid'
    
    table = models.ForeignKey('tables.Table', on_delete=models.CASCADE, related_name='bills')
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='bill')
    cashier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_bills'
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('5.00'),
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))]
    )
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING_PAYMENT,
        db_index=True
    )
    generated_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'bills'
        ordering = ['-generated_at']
        verbose_name = 'Bill'
        verbose_name_plural = 'Bills'
    
    def __str__(self):
        return f"Bill #{self.pk} - Table {self.table.table_number}"
    
    def calculate_totals(self):
        """Calculate subtotal, tax, and total"""
        self.subtotal = self.order.calculate_total()
        self.tax_amount = (self.subtotal * self.tax_percentage) / Decimal('100.00')
        self.total_amount = self.subtotal + self.tax_amount
        self.save()
    
    def mark_as_paid(self, cashier=None):
        """Mark bill as paid and reset table"""
        from django.utils import timezone
        self.status = self.Status.PAID
        self.paid_at = timezone.now()
        if cashier:
            self.cashier = cashier
        self.save()
        
        # Reset table to available
        self.table.mark_as_available()
    
    def save(self, *args, **kwargs):
        """Override save to update table status"""
        is_new = self.pk is None
        if is_new and not self.subtotal:
            self.calculate_totals()
        
        super().save(*args, **kwargs)
        
        if is_new:
            self.table.request_bill()
    
    def export_to_pdf(self):
        """Generate PDF bill"""
        from django.utils import timezone
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph(f"<b>Restaurant Bill</b>", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Bill details
        bill_info = Paragraph(f"""
            <b>Bill #:</b> {self.pk}<br/>
            <b>Table:</b> {self.table.table_number}<br/>
            <b>Date:</b> {self.generated_at.strftime('%Y-%m-%d %H:%M')}<br/>
            <b>Waiter:</b> {self.order.waiter.get_full_name() or self.order.waiter.username}
        """, styles['Normal'])
        elements.append(bill_info)
        elements.append(Spacer(1, 0.3*inch))
        
        # Items table
        data = [['Item', 'Qty', 'Price', 'Subtotal']]
        for item in self.order.items.all():
            data.append([
                item.menu_item.name,
                str(item.quantity),
                f"₹{item.price_at_order:.2f}",
                f"₹{item.subtotal:.2f}"
            ])
        
        # Totals
        data.append(['', '', 'Subtotal:', f"₹{self.subtotal:.2f}"])
        data.append(['', '', f'Tax ({self.tax_percentage}%):', f"₹{self.tax_amount:.2f}"])
        data.append(['', '', 'Total:', f"₹{self.total_amount:.2f}"])
        
        table = Table(data, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -4), 1, colors.black),
            ('LINEABOVE', (2, -3), (-1, -3), 1, colors.black),
            ('LINEABOVE', (2, -1), (-1, -1), 2, colors.black),
            ('FONTNAME', (2, -1), (-1, -1), 'Helvetica-Bold'),
        ]))
        elements.append(table)
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer
