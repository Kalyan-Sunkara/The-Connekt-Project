# Generated by Django 3.1.6 on 2021-08-16 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0009_userprofileinfo_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='progress_type',
            field=models.CharField(choices=[('Active', 'Active'), ('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=12),
        ),
    ]
