# Generated by Django 4.1.7 on 2023-03-07 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense_management', '0002_expense_month_reference'),
    ]

    operations = [
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='expense',
            name='column',
            field=models.CharField(choices=[('PA', 'A pagar'), ('PG', 'Pago')], default='PA', max_length=20),
        ),
    ]
