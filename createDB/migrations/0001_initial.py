# Generated by Django 4.2.13 on 2024-06-23 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('people_num', models.IntegerField()),
                ('tour_type', models.CharField(max_length=10, null=True)),
                ('group_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Group_Members',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='createDB.group')),
            ],
        ),
    ]