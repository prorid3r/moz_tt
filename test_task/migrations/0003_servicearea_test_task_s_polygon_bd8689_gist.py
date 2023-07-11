# Generated by Django 4.2.3 on 2023-07-09 08:45

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_task', '0002_servicearea'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='servicearea',
            index=django.contrib.postgres.indexes.GistIndex(fields=['polygon'], name='test_task_s_polygon_bd8689_gist'),
        ),
    ]
