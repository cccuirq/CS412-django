# Generated by Django 5.1.3 on 2024-11-07 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.TextField()),
                ('first_name', models.TextField()),
                ('street_num', models.IntegerField()),
                ('street_name', models.TextField()),
                ('apt_num', models.IntegerField()),
                ('zip_code', models.IntegerField()),
                ('DOB', models.DateField()),
                ('DOR', models.DateField()),
                ('party_affiliation', models.CharField(max_length=2)),
                ('precinct_num', models.IntegerField()),
                ('v20state', models.BooleanField()),
                ('v21town', models.BooleanField()),
                ('v21primary', models.BooleanField()),
                ('v22general', models.BooleanField()),
                ('v23town', models.BooleanField()),
                ('voter_score', models.IntegerField()),
            ],
        ),
    ]