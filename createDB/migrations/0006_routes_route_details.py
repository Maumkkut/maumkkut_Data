# Generated by Django 4.2.13 on 2024-06-23 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('createDB', '0005_tours'),
    ]

    operations = [
        migrations.AddField(
            model_name='routes',
            name='route_details',
            field=models.ManyToManyField(related_name='get_routes', to='createDB.tours'),
        ),
    ]