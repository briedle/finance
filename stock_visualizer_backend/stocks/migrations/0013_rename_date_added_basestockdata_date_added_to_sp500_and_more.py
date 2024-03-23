# Generated by Django 5.0.3 on 2024-03-23 20:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0012_earningsdata'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basestockdata',
            old_name='date_added',
            new_name='date_added_to_sp500',
        ),
        migrations.AddField(
            model_name='basestockdata',
            name='is_sp500',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='EarningsCalendarData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_date', models.DateField()),
                ('horizon_months', models.IntegerField()),
                ('report_date', models.DateField()),
                ('fiscal_date_ending', models.DateField()),
                ('estimate', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('stock', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='earnings_calendar_data', to='stocks.basestockdata')),
            ],
            options={
                'unique_together': {('stock', 'current_date', 'report_date')},
            },
        ),
    ]
