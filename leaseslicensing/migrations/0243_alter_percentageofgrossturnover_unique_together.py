# Generated by Django 3.2.18 on 2023-08-14 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0242_auto_20230814_1419'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='percentageofgrossturnover',
            unique_together={('year', 'invoicing_details')},
        ),
    ]
