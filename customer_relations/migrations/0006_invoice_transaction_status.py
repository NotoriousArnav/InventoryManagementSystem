# Generated by Django 5.0.1 on 2024-01-16 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_relations', '0005_coupon_invoice_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='transaction_status',
            field=models.BooleanField(default=False),
        ),
    ]
