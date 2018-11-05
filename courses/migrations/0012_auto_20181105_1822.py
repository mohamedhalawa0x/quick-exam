# Generated by Django 2.1.3 on 2018-11-05 18:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_auto_20181105_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='content',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('^[a-zA-Z][a-zA-Z 1-9:]+$', message="Invalid Choice Can't Be Empty or Whitespace")], verbose_name='Choice'),
        ),
    ]