# Generated by Django 3.2.23 on 2023-12-11 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0303_percentageofgrossturnover_estimate_locked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisationcontact',
            name='user_status',
            field=models.CharField(choices=[('draft', 'Draft'), ('pending', 'Pending'), ('active', 'Active'), ('declined', 'Declined'), ('unlinked', 'Unlinked'), ('suspended', 'Suspended'), ('contact_form', 'Contact Form')], default='draft', max_length=40, verbose_name='Status'),
        ),
    ]
