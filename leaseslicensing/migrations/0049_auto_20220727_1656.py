# Generated by Django 3.2.13 on 2022-07-27 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0048_approvaltype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='approvaltype',
            name='description',
        ),
        migrations.RemoveField(
            model_name='approvaltype',
            name='uploaded_date',
        ),
    ]
