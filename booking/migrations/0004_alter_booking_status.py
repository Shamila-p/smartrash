# Generated by Django 4.0.4 on 2022-05-30 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_rename_bin_booking_smartbin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Assigned', 'Assigned '), ('Collected', 'Collected')], max_length=10),
        ),
    ]
