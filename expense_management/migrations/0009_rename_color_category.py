# Generated by Django 4.1.7 on 2023-03-11 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense_management', '0008_color_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Color',
            new_name='Category',
        ),
    ]
