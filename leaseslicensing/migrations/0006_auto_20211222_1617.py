# Generated by Django 3.2.4 on 2021-12-22 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0005_auto_20211217_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='details_text',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='applicationtype',
            name='name',
            field=models.CharField(choices=[('registration_of_interest', 'Registration of Interest'), ('lease', 'Lease'), ('licence', 'Licence')], max_length=64, unique=True),
        ),
    ]
