# Generated by Django 3.2.18 on 2023-07-19 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0217_auto_20230718_1111'),
    ]

    operations = [
        migrations.AddField(
            model_name='cpicalculationmethod',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]
