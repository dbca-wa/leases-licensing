# Generated by Django 3.2.18 on 2023-08-16 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0244_alter_invoice_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='financialquarter',
            name='locked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='percentageofgrossturnover',
            name='locked',
            field=models.BooleanField(default=False),
        ),
    ]
