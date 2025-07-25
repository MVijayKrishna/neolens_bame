# Generated by Django 4.2.20 on 2025-07-16 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JaundicePrediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ethnicity', models.CharField(max_length=50)),
                ('region', models.CharField(max_length=50)),
                ('feeding_pattern', models.CharField(max_length=50)),
                ('sleeping_pattern', models.CharField(max_length=50)),
                ('stooling_pattern', models.CharField(max_length=50)),
                ('urine_color', models.CharField(max_length=50)),
                ('skin_color', models.CharField(max_length=50)),
                ('eye_color', models.CharField(max_length=50)),
                ('prediction', models.CharField(max_length=20)),
                ('confidence', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
