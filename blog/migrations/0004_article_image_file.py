# Generated by Django 5.1.2 on 2024-10-18 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image_file',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
