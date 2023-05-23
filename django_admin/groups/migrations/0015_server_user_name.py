# Generated by Django 4.2.1 on 2023-05-23 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_users_id'),
        ('groups', '0014_remove_server_member_server_created_at_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='user_name',
            field=models.ForeignKey(db_column='user_name', null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.users'),
        ),
    ]
