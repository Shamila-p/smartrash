# Generated by Django 4.0.4 on 2022-05-30 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='Collection_date',
            new_name='collection_date',
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('A', 'Assigned '), ('C', 'Collected')], max_length=1),
        ),
    ]