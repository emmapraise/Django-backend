# Generated by Django 3.2.4 on 2021-07-20 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0029_auto_20210719_2055'),
    ]

    operations = [
        migrations.AddField(
            model_name='installmental_sales',
            name='authorization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='myapi.authcard'),
        ),
    ]
