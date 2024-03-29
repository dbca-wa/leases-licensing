# Generated by Django 3.2.18 on 2023-09-04 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0259_delete_leaselicencefee'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledInvoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('date_to_generate', models.DateField()),
                ('period_start_date', models.DateField()),
                ('period_end_date', models.DateField()),
                ('invoice_has_been_generated', models.BooleanField(default=False)),
                ('attempts_to_send_internal_email', models.PositiveSmallIntegerField(default=0)),
                ('internal_email_sent', models.BooleanField(default=False)),
                ('attempts_to_send_external_email', models.PositiveSmallIntegerField(default=0)),
                ('external_email_sent', models.BooleanField(default=False)),
                ('generated_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scheduled_invoices', to='leaseslicensing.invoicingdetails')),
            ],
            options={
                'ordering': ['date_to_generate'],
            },
        ),
    ]
