# Generated by Django 3.2.4 on 2021-07-19 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0024_auto_20210719_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='installmental_sales',
            name='status',
            field=models.IntegerField(choices=[(0, 'Pending'), (1, 'Paying'), (4, 'Completed'), (3, 'Disapproved')], default=0),
        ),
    ]