# Generated by Django 2.1.3 on 2018-11-05 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20181105_1403'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chapter',
            name='state',
        ),
    ]
