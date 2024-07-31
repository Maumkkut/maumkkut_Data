# Generated by Django 4.2.13 on 2024-07-31 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('createDB', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group_members',
            name='disliked_plans',
        ),
        migrations.RemoveField(
            model_name='group_members',
            name='liked_plans',
        ),
        migrations.RemoveField(
            model_name='routes_plan',
            name='user',
        ),
        migrations.AddField(
            model_name='tour_plan_data',
            name='tour_seq',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
