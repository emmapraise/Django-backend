# Generated by Django 3.2.4 on 2021-07-16 11:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0011_auto_20210716_0031'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='payment',
            name='type',
            field=models.CharField(blank=True, choices=[('Outright Sale', 'Outright Sale'), ('Installmental Sale', 'Installmental Sale'), ('Topup', 'Topup')], max_length=30, null=True),
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('body', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]