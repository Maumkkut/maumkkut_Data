# Generated by Django 4.2.13 on 2024-08-04 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('createDB', '0003_remove_group_members_disliked_plans_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tours',
            name='tour_dislike',
        ),
        migrations.RemoveField(
            model_name='tours',
            name='tour_like',
        ),
    ]
