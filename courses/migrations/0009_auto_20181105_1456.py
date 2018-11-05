# Generated by Django 2.1.3 on 2018-11-05 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_auto_20181105_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='objective',
            field=models.CharField(choices=[('REMINDING', 'Reminding Question'), ('UNDERSTANDING', 'Measure Understanding'), ('CREATIVITY', 'Measure Creativity')], default='REMINDING', max_length=15, verbose_name='Objective of Question'),
        ),
    ]
