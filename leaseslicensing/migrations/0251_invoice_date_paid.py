# Generated by Django 3.2.18 on 2023-08-22 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0250_invoice_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='date_paid',
            field=models.DateTimeField(null=True),
        ),
    ]
