# Generated by Django 4.0.4 on 2022-05-30 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_alter_booking_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='collection_date',
            field=models.DateField(null=True),
        ),
    ]
