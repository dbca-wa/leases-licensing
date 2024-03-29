# Generated by Django 3.2.4 on 2022-02-07 02:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("leaseslicensing", "0029_alter_proposal_submitter"),
    ]

    operations = [
        migrations.CreateModel(
            name="SectionChecklist",
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
                    "section",
                    models.CharField(
                        choices=[
                            ("map", "Map"),
                            ("proposal_details", "Proposal Details"),
                            ("proposal_impact", "Proposal Impact"),
                            ("other", "Other"),
                            ("deed_poll", "Deed Poll"),
                            ("additional_documents", "Additional Documents"),
                        ],
                        default="map",
                        max_length=50,
                        verbose_name="Section",
                    ),
                ),
                (
                    "list_type",
                    models.CharField(
                        choices=[
                            ("assessor_list", "Assessor Checklist"),
                            ("referral_list", "Referral Checklist"),
                        ],
                        default="assessor_list",
                        max_length=30,
                        verbose_name="Checklist type",
                    ),
                ),
                ("enabled", models.BooleanField(default=True)),
                (
                    "application_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="leaseslicensing.applicationtype",
                    ),
                ),
            ],
            options={
                "verbose_name": "Section Questions",
                "verbose_name_plural": "Section Questions",
            },
        ),
        migrations.RenameField(
            model_name="proposalassessmentanswer",
            old_name="assessment",
            new_name="proposal_assessment",
        ),
        migrations.RemoveField(
            model_name="checklistquestion",
            name="checklist_questions",
        ),
        migrations.DeleteModel(
            name="SectionChecklistQuestions",
        ),
        migrations.AddField(
            model_name="checklistquestion",
            name="section_checklist",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="questions",
                to="leaseslicensing.sectionchecklist",
            ),
        ),
    ]
