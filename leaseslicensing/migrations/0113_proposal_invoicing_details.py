# Generated by Django 3.2.13 on 2022-10-05 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0112_auto_20221005_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='invoicing_details',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='leaseslicensing.invoicingdetails'),
        ),
    ]
