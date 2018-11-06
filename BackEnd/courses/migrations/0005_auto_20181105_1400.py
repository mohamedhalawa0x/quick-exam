# Generated by Django 2.1.3 on 2018-11-05 14:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20181105_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='name',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9_.-]*$', message="Invalid Course Name, Can't Be Empty or Whitespace")], verbose_name='Chapter Name'),
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9_.-]*$', message="Invalid Course Name, Can't Be Empty or Whitespace")], verbose_name='Course Name'),
        ),
    ]