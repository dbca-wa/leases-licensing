# Generated by Django 3.2.13 on 2022-09-05 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0082_auto_20220902_1052'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='approvaltypedocumenttypeonapprovaltype',
            unique_together={('approval_type', 'approval_type_document_type')},
        ),
    ]
