# Generated by Django 3.2.13 on 2022-08-18 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0068_auto_20220817_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalrequirement',
            name='reminder_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
