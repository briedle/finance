# Generated by Django 5.0.3 on 2024-03-17 00:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0002_alter_stockdata_volume'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stockdata',
            old_name='adjusted_close_price',
            new_name='adj_close',
        ),
        migrations.RenameField(
            model_name='stockdata',
            old_name='close_price',
            new_name='close',
        ),
        migrations.RenameField(
            model_name='stockdata',
            old_name='high_price',
            new_name='high',
        ),
        migrations.RenameField(
            model_name='stockdata',
            old_name='low_price',
            new_name='low',
        ),
        migrations.RenameField(
            model_name='stockdata',
            old_name='open_price',
            new_name='open',
        ),
    ]
