# Generated by Django 5.1.3 on 2024-11-14 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waterlog', '0002_waterlog_water_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waterlog',
            name='water_type',
            field=models.CharField(choices=[('Cup', 'Cup'), ('Bottle', 'Bottle'), ('L', 'L'), ('ml', 'ml')], default='Plain', max_length=50),
        ),
    ]
