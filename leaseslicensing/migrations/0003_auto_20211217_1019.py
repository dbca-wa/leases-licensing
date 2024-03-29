# Generated by Django 3.2.4 on 2021-12-17 02:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("leaseslicensing", "0002_alter_proposaltype_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="proposaltype",
            name="code",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name="globalsettings",
            name="key",
            field=models.CharField(choices=[], max_length=255),
        ),
        migrations.AlterField(
            model_name="oraclecode",
            name="code_type",
            field=models.CharField(
                choices=[
                    ("registration_of_interest", "registration_of_interest"),
                    ("lease", "lease"),
                    ("licence", "licence"),
                ],
                default="registration_of_interest",
                max_length=64,
                verbose_name="Application Type",
            ),
        ),
        migrations.AlterField(
            model_name="proposal",
            name="proposal_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="leaseslicensing.proposaltype",
            ),
        ),
        migrations.AlterField(
            model_name="proposaltype",
            name="description",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterUniqueTogether(
            name="proposaltype",
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name="proposaltype",
            name="name",
        ),
        migrations.RemoveField(
            model_name="proposaltype",
            name="replaced_by",
        ),
        migrations.RemoveField(
            model_name="proposaltype",
            name="version",
        ),
    ]
