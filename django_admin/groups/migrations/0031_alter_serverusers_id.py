# Generated by Django 4.2.1 on 2023-05-27 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0030_alter_serverusers_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serverusers',
            name='id',
            field=models.CharField(primary_key=True, serialize=False),
        ),
    ]
