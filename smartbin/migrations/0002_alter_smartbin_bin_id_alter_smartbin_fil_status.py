# Generated by Django 4.0.4 on 2022-05-29 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartbin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smartbin',
            name='bin_id',
            field=models.CharField(max_length=36, null=True),
        ),
        migrations.AlterField(
            model_name='smartbin',
            name='fil_status',
            field=models.BooleanField(null=True),
        ),
    ]
