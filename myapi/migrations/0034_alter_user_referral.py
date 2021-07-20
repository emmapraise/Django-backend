# Generated by Django 3.2.4 on 2021-07-20 15:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0033_commission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='referral',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='downline', to=settings.AUTH_USER_MODEL),
        ),
    ]
