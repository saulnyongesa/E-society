# Generated by Django 5.1.5 on 2025-01-25 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_gender_maritalstatus_society_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='society',
            name='address',
        ),
        migrations.RemoveField(
            model_name='society',
            name='certificate_no',
        ),
        migrations.RemoveField(
            model_name='society',
            name='location',
        ),
        migrations.AddField(
            model_name='society',
            name='certificate',
            field=models.ImageField(null=True, upload_to='certificates/'),
        ),
    ]
