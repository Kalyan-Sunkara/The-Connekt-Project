# Generated by Django 3.1.6 on 2021-08-20 04:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('firstApp', '0020_auto_20210820_0401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='rooms',
            name='room_id',
            field=models.CharField(default='3TJXYA', max_length=6, primary_key=True, serialize=False),
        ),
    ]
