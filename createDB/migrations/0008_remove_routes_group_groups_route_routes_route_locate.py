# Generated by Django 4.2.13 on 2024-06-29 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('createDB', '0007_alter_tours_zipcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='routes',
            name='group',
        ),
        migrations.AddField(
            model_name='groups',
            name='route',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='createDB.routes'),
        ),
        migrations.AddField(
            model_name='routes',
            name='route_locate',
            field=models.IntegerField(default='null'),
            preserve_default=False,
        ),
    ]