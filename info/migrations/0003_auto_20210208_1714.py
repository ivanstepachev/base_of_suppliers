# Generated by Django 3.1.6 on 2021-02-08 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0002_article_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='priority',
            field=models.IntegerField(default=1),
        ),
    ]
