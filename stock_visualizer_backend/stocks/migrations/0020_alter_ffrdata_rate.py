# Generated by Django 5.0.3 on 2024-03-24 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0019_ffrdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ffrdata',
            name='rate',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=5, null=True),
        ),
    ]
