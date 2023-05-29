# Generated by Django 4.2.1 on 2023-05-23 08:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_users_id'),
        ('groups', '0015_server_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='Server',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='groups.server'),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.users'),
        ),
    ]