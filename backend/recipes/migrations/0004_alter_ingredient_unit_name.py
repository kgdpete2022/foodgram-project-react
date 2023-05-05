# Generated by Django 3.2.18 on 2023-05-03 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20230503_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='unit_name',
            field=models.CharField(choices=[('gr', 'гр'), ('ml', 'мл'), ('pc', 'шт')], max_length=60, verbose_name='Единица измерения'),
        ),
    ]
