# Generated by Django 4.2.1 on 2023-05-27 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0038_alter_serverusers__id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serverusers',
            name='_id',
            field=models.CharField(db_index=True, default=0, null=True),
        ),
    ]
