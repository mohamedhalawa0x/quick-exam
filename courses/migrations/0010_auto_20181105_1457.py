# Generated by Django 2.1.3 on 2018-11-05 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_auto_20181105_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='score',
            field=models.IntegerField(verbose_name='Question Score'),
        ),
    ]
