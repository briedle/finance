# Generated by Django 5.0.3 on 2024-03-23 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0016_gdpdata'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gdpdata',
            options={'verbose_name': 'US Real GDP (per Capita in 2012 dollars and aggregate)', 'verbose_name_plural': 'US Real GDP (per Capita in 2012 dollars and aggregate) Data'},
        ),
        migrations.AlterField(
            model_name='gdpdata',
            name='value',
            field=models.PositiveBigIntegerField(),
        ),
    ]
