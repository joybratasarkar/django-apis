# Generated by Django 4.2.1 on 2023-05-29 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0046_serverusers__id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='_id',
            field=models.CharField(editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='serverusers',
            name='_id',
            field=models.CharField(db_index=True, default=0, null=True),
        ),
    ]
