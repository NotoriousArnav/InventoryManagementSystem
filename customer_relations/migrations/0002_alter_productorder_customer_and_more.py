# Generated by Django 5.0.1 on 2024-01-16 09:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_relations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productorder',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer_relations.customer'),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='transaction_amount',
            field=models.FloatField(default=1),
        ),
    ]