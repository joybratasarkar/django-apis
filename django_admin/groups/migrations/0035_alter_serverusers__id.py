# Generated by Django 4.2.1 on 2023-05-27 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0034_alter_serverusers__id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serverusers',
            name='_id',
            field=models.BigIntegerField(default=0, null=True),
        ),
    ]
