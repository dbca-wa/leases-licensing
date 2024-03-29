# Generated by Django 3.2.18 on 2023-07-13 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0208_auto_20230713_1408'),
    ]

    operations = [
        migrations.CreateModel(
            name='CPICalculationMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(editable=False, max_length=255)),
                ('display_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='invoicingdetails',
            name='cpi_calculation_method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='invoicing_details', to='leaseslicensing.cpicalculationmethod'),
        ),
    ]
