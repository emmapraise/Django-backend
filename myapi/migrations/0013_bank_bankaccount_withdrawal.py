# Generated by Django 3.2.4 on 2021-07-17 07:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0012_auto_20210716_1257'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=30)),
                ('bank_code', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Withdrawal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipient_code', models.CharField(max_length=100)),
                ('amount', models.CharField(max_length=20)),
                ('account_number', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('status', models.SmallIntegerField(choices=[(0, 'Pending'), (1, 'Approved'), (2, 'Disbursed'), (2, 'Disapproved')], default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bank', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myapi.bank')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=20)),
                ('account_name', models.CharField(blank=True, max_length=100, null=True)),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='myapi.bank')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
