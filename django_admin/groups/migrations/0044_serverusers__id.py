# Generated by Django 4.2.1 on 2023-05-28 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0043_remove_serverusers__id'),
    ]

    operations = [
        migrations.AddField(
            model_name='serverusers',
            name='_id',
            field=models.CharField(db_index=True, null=True),
        ),
    ]