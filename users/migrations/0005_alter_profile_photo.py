# Generated by Django 5.1.5 on 2025-01-19 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='profile_pics/default.jpg', upload_to='profile_pics'),
        ),
    ]
