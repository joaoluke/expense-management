# Generated by Django 4.1.7 on 2023-03-08 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense_management', '0006_alter_expense_column_alter_expense_month_reference'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=255)),
            ],
        ),
        migrations.DeleteModel(
            name='Column',
        ),
    ]
