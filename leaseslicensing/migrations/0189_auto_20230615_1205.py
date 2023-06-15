# Generated by Django 3.2.18 on 2023-06-15 04:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0188_merge_20230608_1650'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='compliance',
            options={'ordering': ('approval__lodgement_number', 'lodgement_number')},
        ),
        migrations.AlterModelOptions(
            name='organisationrequest',
            options={'ordering': ['-lodgement_number'], 'verbose_name': 'Organisation Request'},
        ),
        migrations.AlterField(
            model_name='approval',
            name='status',
            field=models.CharField(choices=[('current', 'Current'), ('current_pending_renewal_review', 'Current (Pending Renewal Review)'), ('current_pending_renewal', 'Current (Pending Renewal)'), ('expired', 'Expired'), ('cancelled', 'Cancelled'), ('surrendered', 'Surrendered'), ('suspended', 'Suspended'), ('extended', 'extended'), ('awaiting_payment', 'Awaiting Payment'), ('current_editing_invoicing', 'Current (Editing Invoicing)')], default='current', max_length=40),
        ),
        migrations.AlterField(
            model_name='compliance',
            name='customer_status',
            field=models.CharField(choices=[('due', 'Due Soon'), ('future', 'Future'), ('with_assessor', 'Under Review'), ('approved', 'Approved'), ('discarded', 'Discarded'), ('overdue', 'Overdue')], default='future', max_length=20),
        ),
        migrations.AlterField(
            model_name='compliance',
            name='processing_status',
            field=models.CharField(choices=[('due', 'Due Soon'), ('future', 'Future'), ('with_assessor', 'With Assessor'), ('approved', 'Approved'), ('discarded', 'Discarded'), ('overdue', 'Overdue')], max_length=20),
        ),
        migrations.CreateModel(
            name='ExternalRefereeInvite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('organisation', models.CharField(max_length=100)),
                ('invite_email_sent', models.BooleanField(default=False)),
                ('datetime_first_logged_in', models.DateTimeField(blank=True, null=True)),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='external_referee_invites', to='leaseslicensing.proposal')),
            ],
            options={
                'verbose_name': 'External Referral',
                'verbose_name_plural': 'External Referrals',
            },
        ),
    ]
