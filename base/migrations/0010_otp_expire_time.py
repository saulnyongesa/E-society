# Generated by Django 5.1.5 on 2025-02-09 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='otp',
            name='expire_time',
            field=models.DateTimeField(null=True),
        ),
    ]
