# Generated by Django 3.2.4 on 2021-07-18 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0020_auto_20210718_1818'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='refferal',
            new_name='referral',
        ),
    ]
