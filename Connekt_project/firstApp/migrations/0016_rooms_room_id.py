# Generated by Django 3.1.6 on 2021-08-19 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0015_question_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='rooms',
            name='room_id',
            field=models.CharField(default='169NKY', max_length=6),
        ),
    ]
