# Generated by Django 3.2.18 on 2023-05-11 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0166_merge_20230509_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalgeometry',
            name='drawn_by',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
