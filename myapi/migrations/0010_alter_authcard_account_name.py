# Generated by Django 3.2.4 on 2021-07-15 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0009_authcard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authcard',
            name='account_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
