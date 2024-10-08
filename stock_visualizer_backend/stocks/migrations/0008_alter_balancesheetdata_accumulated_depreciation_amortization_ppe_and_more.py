# Generated by Django 5.0.3 on 2024-03-23 14:25

import stocks.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0007_alter_incomestatementdata_cogs_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balancesheetdata',
            name='accumulated_depreciation_amortization_ppe',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='capital_lease_obligations',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='cash_and_cash_equivalents_at_carrying_value',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='cash_and_short_term_investments',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='common_stock',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='common_stock_shares_outstanding',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='current_accounts_payable',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='current_debt',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='current_long_term_debt',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='current_net_receivables',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='deferred_revenue',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='goodwill',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='intangible_assets',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='intangible_assets_excluding_goodwill',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='inventory',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='investments',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='long_term_debt',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='long_term_debt_noncurrent',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='long_term_investments',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='other_current_assets',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='other_current_liabilities',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='other_non_current_assets',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='other_non_current_liabilities',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='property_plant_equipment',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='retained_earnings',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='short_long_term_debt_total',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='short_term_debt',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='short_term_investments',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='total_assets',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='total_current_assets',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='total_current_liabilities',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='total_liabilities',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='total_non_current_assets',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='total_non_current_liabilities',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='total_shareholder_equity',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheetdata',
            name='treasury_stock',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incomestatementdata',
            name='cogs',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incomestatementdata',
            name='comprehensive_income',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incomestatementdata',
            name='cost_of_revenue',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incomestatementdata',
            name='depreciation',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incomestatementdata',
            name='depreciation_amortization',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incomestatementdata',
            name='ebit',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incomestatementdata',
            name='ebitda',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incomestatementdata',
            name='gross_profit',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incomestatementdata',
            name='income_before_tax',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incomestatementdata',
            name='income_tax_expense',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incomestatementdata',
            name='interest_and_debt_expense',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incomestatementdata',
            name='interest_expense',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incomestatementdata',
            name='interest_income',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incomestatementdata',
            name='net_income',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incomestatementdata',
            name='net_income_from_continuing_operations',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incomestatementdata',
            name='net_interest_income',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incomestatementdata',
            name='net_investment_income',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incomestatementdata',
            name='non_interest_income',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incomestatementdata',
            name='operating_income',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incomestatementdata',
            name='other_non_operating_income',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incomestatementdata',
            name='total_revenue',
            field=stocks.models.StockIntegerField(blank=True, null=True),
        ),
    ]
