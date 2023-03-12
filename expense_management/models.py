from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, default="")
    color = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Expense(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PAID', 'Paid'),
        ('PENDING', 'Pending'),
        ('OVERDUE', 'Overdue'),
    ]
    MONTHS_CHOICES = [
        (1, 'Janeiro'),
        (2, 'Fevereiro'),
        (3, 'Março'),
        (4, 'Abril'),
        (5, 'Maio'),
        (6, 'Junho'),
        (7, 'Julho'),
        (8, 'Agosto'),
        (9, 'Setembro'),
        (10, 'Outubro'),
        (11, 'Novembro'),
        (12, 'Dezembro'),
    ]
    COLUMN_CHOICES = (
        ('TO_PAY', 'A pagar'),
        ('PAID', 'Pago')
    )

    name = models.CharField(max_length=255)
    value = models.DecimalField(decimal_places=2, max_digits=10)
    invoice_due_date = models.DateField()
    category = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    column = models.CharField(max_length=20, choices=COLUMN_CHOICES, default=COLUMN_CHOICES[0][0])
    month_reference = models.PositiveSmallIntegerField(
        choices=MONTHS_CHOICES, default='1')
    payment_status = models.CharField(
        max_length=10, choices=PAYMENT_STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return self.name