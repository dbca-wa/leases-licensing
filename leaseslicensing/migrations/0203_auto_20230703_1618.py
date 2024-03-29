# Generated by Django 3.2.18 on 2023-07-03 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0202_alter_compliance_processing_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitiveprocess',
            name='site_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='leaseslicensing.sitename'),
        ),
        migrations.CreateModel(
            name='CompetitiveProcessGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competitive_process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='leaseslicensing.competitiveprocess')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='leaseslicensing.group')),
            ],
            options={
                'unique_together': {('competitive_process', 'group')},
            },
        ),
    ]
