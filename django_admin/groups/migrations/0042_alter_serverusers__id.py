# Generated by Django 4.2.1 on 2023-05-28 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0041_alter_serverusers__id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serverusers',
            name='_id',
            field=models.IntegerField(null=True),
        ),
    ]
