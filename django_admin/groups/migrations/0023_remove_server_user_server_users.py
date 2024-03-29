# Generated by Django 4.2.1 on 2023-05-24 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_users_id'),
        ('groups', '0022_alter_server__id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='user',
        ),
        migrations.AddField(
            model_name='server',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='servers', to='authentication.users'),
        ),
    ]
