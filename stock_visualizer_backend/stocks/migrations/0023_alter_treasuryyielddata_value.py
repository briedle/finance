# Generated by Django 5.0.3 on 2024-03-24 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0022_treasuryyielddata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='treasuryyielddata',
            name='value',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=6, null=True),
        ),
    ]
