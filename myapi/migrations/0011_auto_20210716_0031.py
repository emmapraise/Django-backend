# Generated by Django 3.2.4 on 2021-07-15 23:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0010_alter_authcard_account_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='sale',
        ),
        migrations.AddField(
            model_name='payment',
            name='type',
            field=models.CharField(blank=True, choices=[('Sales', 'Sales'), ('Topup', 'Topup')], max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='wallet_balance',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapi.product'),
        ),
        migrations.AlterField(
            model_name='saved',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapi.product'),
        ),
        migrations.DeleteModel(
            name='Installmental_sales',
        ),
    ]
