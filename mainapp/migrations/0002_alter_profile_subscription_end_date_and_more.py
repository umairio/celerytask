# Generated by Django 5.0 on 2024-03-07 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='subscription_end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='subscription_start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
