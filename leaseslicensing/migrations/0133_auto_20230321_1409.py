# Generated by Django 3.2.18 on 2023-03-21 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0132_alter_organisationrequest_assigned_officer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organisationrequestdeclineddetails',
            old_name='request',
            new_name='organisation_request',
        ),
        migrations.AlterField(
            model_name='organisationrequest',
            name='assigned_officer',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
