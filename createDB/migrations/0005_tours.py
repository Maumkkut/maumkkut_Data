# Generated by Django 4.2.13 on 2024-06-23 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('createDB', '0004_rename_group_name_routes_route_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sigungucode', models.IntegerField()),
                ('addr1', models.TextField()),
                ('addr2', models.TextField()),
                ('image', models.TextField(null=True)),
                ('cat1', models.CharField(max_length=3)),
                ('cat2', models.CharField(max_length=5)),
                ('cat3', models.CharField(max_length=9)),
                ('type_id', models.IntegerField()),
                ('mapx', models.FloatField()),
                ('mapy', models.FloatField()),
                ('title', models.TextField(null=True)),
                ('zipcode', models.IntegerField(null=True)),
                ('tel', models.TextField(null=True)),
                ('eventstartdate', models.DateTimeField(null=True)),
                ('eventenddate', models.DateTimeField(null=True)),
            ],
        ),
    ]
