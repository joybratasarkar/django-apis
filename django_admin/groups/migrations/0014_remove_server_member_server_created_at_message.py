# Generated by Django 4.2.1 on 2023-05-21 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('groups', '0013_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='member',
        ),
        migrations.AddField(
            model_name='server',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('Server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.server')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.users')),
            ],
        ),
    ]
