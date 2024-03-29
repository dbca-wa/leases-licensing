# Generated by Django 3.2.13 on 2022-08-12 03:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0060_leaselicenceapprovaldocument_leaselicenceapprovaldocumentcollection'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='leaselicenceapprovaldocumentcollection',
            options={'verbose_name': 'Lease Licence Approval Document Collection', 'verbose_name_plural': 'Lease Licence Approval Document Collections'},
        ),
        migrations.AddField(
            model_name='leaselicenceapprovaldocumentcollection',
            name='approval_type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='lease_licence_approval_document_collection', to='leaseslicensing.approvaltype'),
            preserve_default=False,
        ),
    ]
