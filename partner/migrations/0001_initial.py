# Generated by Django 3.1.6 on 2021-02-01 23:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_partner', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=43)),
                ('code', models.CharField(default='', max_length=12)),
                ('balance', models.IntegerField(default=0)),
                ('date', models.DateField(auto_now_add=True)),
                ('mentor', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='partners', to='partner.partner')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
