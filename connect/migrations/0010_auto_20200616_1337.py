# Generated by Django 3.0.6 on 2020-06-16 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connect', '0009_blogs_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogs_model',
            name='operating_time',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='blogs_model',
            name='total_emp',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
