# Generated by Django 3.2.13 on 2022-08-26 01:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0076_rename_competitive_process_proposal_generated_competitive_process'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitiveprocess',
            name='generated_proposal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='leaseslicensing.proposal'),
        ),
    ]
