# Generated by Django 4.2.13 on 2024-08-26 13:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('createDB', '0004_remove_tours_tour_dislike_remove_tours_tour_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_age', models.IntegerField(null=True)),
                ('user_type', models.TextField(null=True)),
                ('user_healing', models.IntegerField(null=True)),
                ('user_relax', models.IntegerField(null=True)),
                ('user_nature', models.IntegerField(null=True)),
                ('user_exhibit', models.IntegerField(null=True)),
                ('user_food', models.IntegerField(null=True)),
                ('user_adventure', models.IntegerField(null=True)),
                ('user_people', models.IntegerField(null=True)),
                ('user_shopping', models.IntegerField(null=True)),
                ('user_photo', models.IntegerField(null=True)),
                ('tour_dislike', models.ManyToManyField(related_name='disliked_users', to='createDB.tours')),
                ('tour_like', models.ManyToManyField(related_name='liked_users', to='createDB.tours')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
