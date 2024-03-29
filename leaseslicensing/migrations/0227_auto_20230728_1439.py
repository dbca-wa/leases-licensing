# Generated by Django 3.2.18 on 2023-07-28 06:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0226_auto_20230728_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoicingdetails',
            name='invoicing_day_of_month',
            field=models.PositiveSmallIntegerField(blank=True, default=1, help_text='Day of the month to generate invoices.', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(28)]),
        ),
        migrations.AlterField(
            model_name='invoicingdetails',
            name='invoicing_month_of_year',
            field=models.PositiveSmallIntegerField(blank=True, default=1, help_text='Month of the year to generate invoices.', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)]),
        ),
    ]
