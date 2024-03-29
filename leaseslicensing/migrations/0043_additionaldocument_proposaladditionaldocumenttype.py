# Generated by Django 3.2.12 on 2022-03-11 06:20

from django.db import migrations, models
import django.db.models.deletion
import leaseslicensing.components.proposals.models


class Migration(migrations.Migration):

    dependencies = [
        ("leaseslicensing", "0042_maplayer_transparency"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProposalAdditionalDocumentType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "additional_document_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="leaseslicensing.additionaldocumenttype",
                    ),
                ),
                (
                    "proposal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="leaseslicensing.proposal",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AdditionalDocument",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=255, verbose_name="name"),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
                ("uploaded_date", models.DateTimeField(auto_now_add=True)),
                (
                    "_file",
                    models.FileField(
                        max_length=512,
                        upload_to=leaseslicensing.components.proposals.models.update_additional_doc_filename,
                    ),
                ),
                (
                    "proposal_additional_document_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="leaseslicensing.proposaladditionaldocumenttype",
                    ),
                ),
            ],
        ),
    ]
