# Generated by Django 5.0.1 on 2024-01-13 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.FloatField(default=100),
        ),
        migrations.AddField(
            model_name='product',
            name='qty',
            field=models.IntegerField(default=1),
        ),
    ]
