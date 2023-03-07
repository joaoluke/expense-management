from django.db import models

# Create your models here.
class Expense(models.Model):
    name = models.CharField(max_length=255)
    value = models.DecimalField(decimal_places=2, max_digits=10)
    invoice_due_date = models.DateField()
    category = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    PAYMENT_STATUS_CHOICES = [
        ('PAID', 'Paid'),
        ('PENDING', 'Pending'),
        ('OVERDUE', 'Overdue'),
    ]
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return self.name