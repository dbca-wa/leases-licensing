# Generated by Django 3.2.13 on 2022-09-19 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0089_merge_20220913_1129'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChargeMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=200, unique=True)),
            ],
        ),
    ]
