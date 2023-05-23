# Generated by Django 4.2.1 on 2023-05-22 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_users_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='id',
        ),
        migrations.AlterField(
            model_name='users',
            name='user_name',
            field=models.CharField(max_length=255, primary_key=True, serialize=False, unique=True),
        ),
    ]