# Generated by Django 3.2.23 on 2024-01-31 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0319_delete_crownlandrentreviewdate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compliance',
            name='num_participants',
        ),
    ]
