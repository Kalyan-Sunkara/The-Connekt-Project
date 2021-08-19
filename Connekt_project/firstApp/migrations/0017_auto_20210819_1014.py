# Generated by Django 3.1.6 on 2021-08-19 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0016_rooms_room_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='rooms',
            name='slug',
            field=models.SlugField(null=True),
        ),
        migrations.AlterField(
            model_name='rooms',
            name='room_id',
            field=models.CharField(default='HM0UEE', max_length=6),
        ),
    ]
