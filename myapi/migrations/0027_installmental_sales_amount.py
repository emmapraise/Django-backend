# Generated by Django 3.2.4 on 2021-07-19 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0026_payment_install_sale'),
    ]

    operations = [
        migrations.AddField(
            model_name='installmental_sales',
            name='amount',
            field=models.FloatField(default=0),
        ),
    ]