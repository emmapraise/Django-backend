# Generated by Django 3.2.4 on 2021-07-19 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0025_installmental_sales_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='install_sale',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapi.installmental_sales'),
        ),
    ]
