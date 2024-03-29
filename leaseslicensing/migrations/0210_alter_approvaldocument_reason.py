# Generated by Django 3.2.18 on 2023-08-10 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0209_auto_20230807_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvaldocument',
            name='reason',
            field=models.CharField(choices=[('new', 'New'), ('amended', 'Amended'), ('renewed', 'Renewed'), ('renewed', 'Reissued'), ('invoicing_updated', 'Invoicing updated')], default='new', max_length=25),
        ),
    ]
