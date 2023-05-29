# Generated by Django 4.2.1 on 2023-05-23 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_users_id'),
        ('groups', '0018_remove_server__id_alter_server_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='user_name',
        ),
        migrations.AddField(
            model_name='server',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='joined_servers', to='authentication.users'),
        ),
        migrations.AddField(
            model_name='server',
            name='user',
            field=models.ForeignKey(db_column='user_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_servers', to='authentication.users'),
        ),
    ]
