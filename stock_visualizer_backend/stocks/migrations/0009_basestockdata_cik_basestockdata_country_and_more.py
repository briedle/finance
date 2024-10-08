# Generated by Django 5.0.3 on 2024-03-23 17:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0008_alter_balancesheetdata_accumulated_depreciation_amortization_ppe_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='basestockdata',
            name='cik',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='basestockdata',
            name='country',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='basestockdata',
            name='currency',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='basestockdata',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='basestockdata',
            name='exchange',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='basestockdata',
            name='fiscal_year_end',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='basestockdata',
            name='industry',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='basestockdata',
            name='date_added',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='basestockdata',
            name='sector',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='QuarterlyStockOverview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quarter_end_date', models.DateField()),
                ('market_capitalization', models.BigIntegerField(blank=True, null=True)),
                ('ebitda', models.BigIntegerField(blank=True, null=True)),
                ('pe_ratio', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('peg_ratio', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('book_value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('dividend_per_share', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('dividend_yield', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('eps', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('revenue_per_share_ttm', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('profit_margin', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('operating_margin_ttm', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('return_on_assets_ttm', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('return_on_equity_ttm', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('revenue_ttm', models.BigIntegerField(blank=True, null=True)),
                ('gross_profit_ttm', models.BigIntegerField(blank=True, null=True)),
                ('diluted_eps_ttm', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('quarterly_earnings_growth_yoy', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('quarterly_revenue_growth_yoy', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('analyst_target_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('analyst_rating_strong_buy', models.IntegerField(blank=True, null=True)),
                ('analyst_rating_buy', models.IntegerField(blank=True, null=True)),
                ('analyst_rating_hold', models.IntegerField(blank=True, null=True)),
                ('analyst_rating_sell', models.IntegerField(blank=True, null=True)),
                ('analyst_rating_strong_sell', models.IntegerField(blank=True, null=True)),
                ('trailing_pe', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('forward_pe', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('price_to_sales_ratio_ttm', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('price_to_book_ratio', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('ev_to_revenue', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('ev_to_ebitda', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('beta', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('week_high_52', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('week_low_52', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('day_moving_average_50', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('day_moving_average_200', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('shares_outstanding', models.BigIntegerField(blank=True, null=True)),
                ('dividend_date', models.DateField(blank=True, null=True)),
                ('ex_dividend_date', models.DateField(blank=True, null=True)),
                ('stock', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stock_overview', to='stocks.basestockdata')),
            ],
            options={
                'unique_together': {('stock', 'quarter_end_date')},
            },
        ),
    ]
