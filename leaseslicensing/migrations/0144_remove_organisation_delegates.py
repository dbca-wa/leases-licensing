# Generated by Django 3.2.18 on 2023-04-11 02:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0143_remove_organisationrequest_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisation',
            name='delegates',
        ),
    ]