# Generated by Django 4.2.1 on 2023-05-22 05:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='name',
            new_name='user_name',
        ),
    ]