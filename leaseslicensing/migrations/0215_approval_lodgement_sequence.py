# Generated by Django 3.2.18 on 2023-08-16 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0214_alter_approvaldocument_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='approval',
            name='lodgement_sequence',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
