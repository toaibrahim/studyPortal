# Generated by Django 4.0.3 on 2022-04-05 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_homework'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
