# Generated by Django 3.2.13 on 2022-10-21 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0115_auto_20221007_0943'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='crownlandrentreviewdate',
            options={'ordering': ['review_date']},
        ),
        migrations.AlterModelOptions(
            name='fixedannualincrementamount',
            options={'ordering': ['year']},
        ),
        migrations.AlterModelOptions(
            name='fixedannualincrementpercentage',
            options={'ordering': ['year']},
        ),
        migrations.AlterModelOptions(
            name='percentageofgrossturnover',
            options={'ordering': ['year']},
        ),
        migrations.AlterField(
            model_name='proposalassessment',
            name='proposal',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='assessment', to='leaseslicensing.proposal'),
        ),
    ]
