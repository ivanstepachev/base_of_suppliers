# Generated by Django 3.1.6 on 2021-02-01 23:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partner',
            name='mentor',
        ),
    ]
