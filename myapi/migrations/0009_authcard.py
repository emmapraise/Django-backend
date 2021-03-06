# Generated by Django 3.2.4 on 2021-07-15 12:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0008_auto_20210713_2223'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authorization_code', models.CharField(max_length=30)),
                ('card_type', models.CharField(max_length=30)),
                ('last4', models.IntegerField()),
                ('exp_month', models.CharField(max_length=2)),
                ('exp_year', models.CharField(max_length=4)),
                ('bin', models.CharField(max_length=30)),
                ('bank', models.CharField(max_length=30)),
                ('channel', models.CharField(max_length=30)),
                ('signature', models.CharField(max_length=30)),
                ('is_reusable', models.BooleanField(default=False)),
                ('country_code', models.CharField(max_length=30)),
                ('account_name', models.CharField(max_length=50)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
