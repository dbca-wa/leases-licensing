# Generated by Django 3.2.13 on 2022-08-12 08:35

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0058_merge_20220810_1159'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetitiveProcessGeometry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polygon', django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=4326)),
                ('competitive_process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competitive_process_geometries', to='leaseslicensing.competitiveprocess')),
            ],
        ),
    ]
