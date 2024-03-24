# models.py
from django.db import models

# Create your models here.

class StockDecimalField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        # Set default values for max_digits and decimal_places
        kwargs.setdefault('max_digits', 15)
        kwargs.setdefault('decimal_places', 2)
        kwargs.setdefault('null', True)
        kwargs.setdefault('blank', True)
        super().__init__(*args, **kwargs)

class StockIntegerField(models.BigIntegerField):
    def __init__(self, *args, **kwargs):
        # Set default values for null and blank
        kwargs.setdefault('null', True)
        kwargs.setdefault('blank', True)
        super().__init__(*args, **kwargs)


class BaseStockData(models.Model):
    symbol = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    headquarters = models.CharField(max_length=255)
    cik = models.CharField(max_length=20, null=True, blank=True)
    exchange = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    currency = models.CharField(max_length=10, null=True, blank=True)
    sector = models.CharField(max_length=100, null=True, blank=True)
    industry = models.CharField(max_length=255, null=True, blank=True)
    fiscal_year_end = models.CharField(max_length=20, null=True, blank=True)
    is_sp500 = models.BooleanField(default=False)
    date_added_to_sp500 = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.symbol} - {self.name}"


class QuarterlyStockOverview(models.Model):
    stock = models.ForeignKey(
        BaseStockData,
        on_delete=models.CASCADE,
        related_name='stock_overview',
        null=True,
    )
    quarter_end_date = models.DateField()
    market_capitalization = models.BigIntegerField(null=True, blank=True)
    ebitda = models.BigIntegerField(null=True, blank=True)
    pe_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    peg_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    book_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dividend_per_share = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dividend_yield = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    eps = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    revenue_per_share_ttm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    profit_margin = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    operating_margin_ttm = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    return_on_assets_ttm = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    return_on_equity_ttm = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    revenue_ttm = models.BigIntegerField(null=True, blank=True)
    gross_profit_ttm = models.BigIntegerField(null=True, blank=True)
    diluted_eps_ttm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quarterly_earnings_growth_yoy = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    quarterly_revenue_growth_yoy = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    analyst_target_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    analyst_rating_strong_buy = models.IntegerField(null=True, blank=True)
    analyst_rating_buy = models.IntegerField(null=True, blank=True)
    analyst_rating_hold = models.IntegerField(null=True, blank=True)
    analyst_rating_sell = models.IntegerField(null=True, blank=True)
    analyst_rating_strong_sell = models.IntegerField(null=True, blank=True)
    trailing_pe = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    forward_pe = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_to_sales_ratio_ttm = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    price_to_book_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ev_to_revenue = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ev_to_ebitda = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    beta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    week_high_52 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    week_low_52 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    day_moving_average_50 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    day_moving_average_200 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    shares_outstanding = models.BigIntegerField(null=True, blank=True)
    dividend_date = models.DateField(null=True, blank=True)
    ex_dividend_date = models.DateField(null=True, blank=True)
    
    class Meta:
        unique_together = ('stock', 'quarter_end_date')

    def __str__(self):
        return f"{self.stock.symbol} ({self.quarter_end_date})"


class StockPriceData(models.Model):
    INTERVAL_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    stock = models.ForeignKey(
        BaseStockData,
        on_delete=models.CASCADE,
        related_name='price_data',
        null=True,
    )
    date = models.DateField()
    interval = models.CharField(max_length=7, choices=INTERVAL_CHOICES, default='monthly')
    open = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    adj_close = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()
    dividend = models.DecimalField(max_digits=10, decimal_places=2)
    split_coefficient = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('stock', 'date', 'interval')

    def __str__(self):
        return f"{self.stock.symbol} - {self.date} ({self.interval})"


# class MonthlyStockPriceData(models.Model):
#     stock = models.ForeignKey(
#         BaseStockData,
#         on_delete=models.CASCADE,
#         related_name='monthly_price_data',
#         null=True,
#         )
#     date = models.DateField()
#     open = models.DecimalField(max_digits=10, decimal_places=2)
#     high = models.DecimalField(max_digits=10, decimal_places=2)
#     low = models.DecimalField(max_digits=10, decimal_places=2)
#     close = models.DecimalField(max_digits=10, decimal_places=2)
#     adj_close = models.DecimalField(max_digits=10, decimal_places=2)
#     volume = models.BigIntegerField()
#     dividend = models.DecimalField(max_digits=10, decimal_places=2)  
#     class Meta:
#         unique_together = ('stock', 'date')

#     def __str__(self):
#         return f"{self.stock.symbol} - {self.date}"


# We are going to use this metaclass to construct the IncomeStatementData and BalanceSheetData classes
class FinancialDataMeta(type(models.Model)):
    def __new__(cls, name, bases, attrs):
        # Check if the class has a 'financial_fields' attribute
        financial_fields = attrs.pop('financial_fields', [])
        
        for field_name in financial_fields:
            attrs[field_name] = StockIntegerField()
        
        return super().__new__(cls, name, bases, attrs)

# Example usage:

class IncomeStatementData(models.Model, metaclass=FinancialDataMeta):
    REPORT_TYPE_CHOICES = [
        ('annual', 'Annual'),
        ('quarterly', 'Quarterly'),
    ]
    stock = models.ForeignKey(
        BaseStockData,
        on_delete=models.CASCADE,
        related_name='income_statement_data',
        null=True,
    )
    report_type = models.CharField(max_length=9, choices=REPORT_TYPE_CHOICES)
    date = models.DateField()
    
    financial_fields = [
        'gross_profit',
        'total_revenue',
        'cost_of_revenue',
        'cogs',
        'operating_income',
        'net_investment_income',
        'net_interest_income',
        'interest_income',
        'interest_expense',
        'non_interest_income',
        'other_non_operating_income',
        'depreciation',
        'depreciation_amortization',
        'income_before_tax',
        'income_tax_expense',
        'interest_and_debt_expense',
        'net_income_from_continuing_operations',
        'comprehensive_income',
        'ebit',
        'ebitda',
        'net_income',
    ]
    class Meta:
        unique_together = ('stock', 'report_type', 'date')

class BalanceSheetData(models.Model, metaclass=FinancialDataMeta):
    REPORT_TYPE_CHOICES = [
        ('annual', 'Annual'),
        ('quarterly', 'Quarterly'),
    ]
    stock = models.ForeignKey(
        BaseStockData,
        on_delete=models.CASCADE,
        related_name='balance_sheet_data',
        null=True,
    )
    report_type = models.CharField(max_length=9, choices=REPORT_TYPE_CHOICES)
    date = models.DateField()

    financial_fields = [
        'total_assets',
        'total_current_assets',
        'cash_and_cash_equivalents_at_carrying_value',
        'cash_and_short_term_investments',
        'inventory',
        'current_net_receivables',
        'total_non_current_assets',
        'property_plant_equipment',
        'accumulated_depreciation_amortization_ppe',
        'intangible_assets',
        'intangible_assets_excluding_goodwill',
        'goodwill',
        'investments',
        'long_term_investments',
        'short_term_investments',
        'other_current_assets',
        'other_non_current_assets',
        'total_liabilities',
        'total_current_liabilities',
        'current_accounts_payable',
        'deferred_revenue',
        'current_debt',
        'short_term_debt',
        'total_non_current_liabilities',
        'capital_lease_obligations',
        'long_term_debt',
        'current_long_term_debt',
        'long_term_debt_noncurrent',
        'short_long_term_debt_total',
        'other_current_liabilities',
        'other_non_current_liabilities',
        'total_shareholder_equity',
        'treasury_stock',
        'retained_earnings',
        'common_stock',
        'common_stock_shares_outstanding',
    ]
    class Meta:
        unique_together = ('stock', 'report_type', 'date')


class CashFlowData(models.Model, metaclass=FinancialDataMeta):
    REPORT_TYPE_CHOICES = [
        ('annual', 'Annual'),
        ('quarterly', 'Quarterly'),
    ]
    stock = models.ForeignKey(
        BaseStockData,
        on_delete=models.CASCADE,
        related_name='cash_flow_data',
        null=True,
    )
    report_type = models.CharField(max_length=9, choices=REPORT_TYPE_CHOICES)
    date = models.DateField()

    financial_fields = [
        'operating_cashflow',
        'payments_for_operating_activities',
        'proceeds_from_operating_activities',
        'change_in_operating_liabilities',
        'change_in_operating_assets',
        'depreciation_depletion_and_amortization',
        'capital_expenditures',
        'change_in_receivables',
        'change_in_inventory',
        'profit_loss',
        'cashflow_from_investment',
        'cashflow_from_financing',
        'proceeds_from_repayments_of_short_term_debt',
        'payments_for_repurchase_of_common_stock',
        'payments_for_repurchase_of_equity',
        'payments_for_repurchase_of_preferred_stock',
        'dividend_payout',
        'dividend_payout_common_stock',
        'dividend_payout_preferred_stock',
        'proceeds_from_issuance_of_common_stock',
        'proceeds_issuance_long_term_debt_capital_sec_net',
        'proceeds_from_issuance_of_preferred_stock',
        'proceeds_from_repurchase_of_equity',
        'proceeds_from_sale_of_treasury_stock',
        'change_in_cash_and_cash_equivalents',
        'change_in_exchange_rate',
        'net_income',
    ]
    class Meta:
        unique_together = ('stock', 'report_type', 'date')

    def __str__(self):
        return f"{self.stock.symbol} - {self.report_type} - {self.date}"

class EarningsData(models.Model, metaclass=FinancialDataMeta):
    REPORT_TYPE_CHOICES = [
        ('annual', 'Annual'),
        ('quarterly', 'Quarterly'),
    ]

    stock = models.ForeignKey(
        BaseStockData,
        on_delete=models.CASCADE,
        related_name='earnings_data',
        null=True,
    )
    report_type = models.CharField(max_length=9, choices=REPORT_TYPE_CHOICES)
    date = models.DateField()
    reported_date = models.DateField(null=True, blank=True)  # Only for quarterly data
    reported_eps = StockIntegerField()
    estimated_eps = StockIntegerField(null=True, blank=True)  # Only for quarterly data
    surprise = StockIntegerField(null=True, blank=True)  # Only for quarterly data
    surprise_percentage = StockIntegerField(null=True, blank=True)  # Only for quarterly data

    financial_fields = [
        'reported_eps',
        'estimated_eps',
        'surprise',
        'surprise_percentage',
    ]

    class Meta:
        unique_together = ('stock', 'report_type', 'date', 'reported_date')


class EarningsCalendarData(models.Model):
    stock = models.ForeignKey(
        BaseStockData,
        on_delete=models.CASCADE,
        related_name='earnings_calendar_data',
        null=True,
    )
    current_date = models.DateField()
    horizon_months = models.IntegerField()
    report_date = models.DateField()
    fiscal_date_ending = models.DateField()
    estimate = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return f"{self.name} ({self.symbol}) - {self.report_date}"
    
    class Meta:
        unique_together = ('stock', 'current_date', 'report_date')


class GDPData(models.Model): 
    REPORT_TYPE_CHOICES = [
        ('annual', 'Annual'),
        ('quarterly', 'Quarterly'),
    ]
    
    date = models.DateField()
    interval = models.CharField(max_length=10, choices=REPORT_TYPE_CHOICES)  # 'annual' or 'quarterly'
    per_capita = models.BooleanField()
    value = models.PositiveBigIntegerField()
    # value = models.DecimalField(max_digits=20, decimal_places=)

    class Meta:
        verbose_name = "US Real GDP (per Capita in 2012 dollars and aggregate)"
        verbose_name_plural = "US Real GDP (per Capita in 2012 dollars and aggregate) Data"
        unique_together = ('date', 'interval', 'per_capita')

    def __str__(self):
        return f"Real GDP{' Per Capita (2012 dollars) ' if self.per_capita else ''} on {self.date} ({self.interval})"
    

class TreasuryYieldData(models.Model):
    date = models.DateField()
    maturity_months = models.IntegerField()
    value = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)  # Adjust max_digits and decimal_places as needed


    class Meta:
        unique_together = ('date', 'maturity_months')
        verbose_name = "Treasury Yield"
        verbose_name_plural = "Treasury Yields"

    def __str__(self):
        return f"{self.maturity_months} months yield on {self.date}: {100 * self.value}%"



class FFRData(models.Model):
    date = models.DateField(unique=True)
    value = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)

    def __str__(self):
        try:
            percent = 100 * self.value
        except TypeError:
            percent = 'Unknown'
        return f"{self.date}: {percent}%"

    class Meta:
        verbose_name = "Effective Federal Funds Rate"
        verbose_name_plural = "Effective Federal Funds Rate Data"
        ordering = ['-date']


class CPIData(models.Model):
    date = models.DateField(unique=True)
    value = models.DecimalField(max_digits=9, decimal_places=5)

    class Meta:
        verbose_name = "Consumer Price Index for All Urban Consumers (1982-1984=1)"
        verbose_name_plural = "Consumer Price Index (1982-1984=1) Data"
        get_latest_by = "date"
        ordering = ['-date']

    def __str__(self):
        return f"CPI for {self.date}: {self.value}"



class InflationData(models.Model):
    date = models.DateField(unique=True)
    value = models.DecimalField(max_digits=9, decimal_places=5)  # Inflation values are percentages, stored as decimals

    class Meta:
        verbose_name = "Inflation Rate"
        verbose_name_plural = "Inflation Rate Data"
        ordering = ['-date']

    def __str__(self):
        try:
            percent = 100 * self.rate
        except TypeError:
            percent = 'Unknown'
        return f"{self.date}: {percent}%"

class RetailSalesData(models.Model):
    date = models.DateField(unique=True)
    value = models.BigIntegerField()  

    class Meta:
        verbose_name = "Retail Sales"
        verbose_name_plural = "Retail Sales Data"
        ordering = ['-date']

    def __str__(self):
        return f"{self.date} - ${self.value}"

class DurablesData(models.Model):
    date = models.DateField(unique=True)
    value = models.BigIntegerField() 

    class Meta:
        verbose_name = "Durable Goods Orders"
        verbose_name_plural = "Durable Goods Orders Data"
        ordering = ['-date']

    def __str__(self):
        return f"{self.date} - ${self.value}"

class UnemploymentData(models.Model):
    date = models.DateField(unique=True)
    value = models.DecimalField(max_digits=4, decimal_places=1)  

    class Meta:
        verbose_name = "Unemployment Rate"
        verbose_name_plural = "Unemployment Rate Data"
        ordering = ['-date']

    def __str__(self):
        try:
            percent = 100 * self.rate
        except TypeError:
            percent = 'Unknown'
        return f"{self.date}: {percent}%"

class NonfarmPayrollData(models.Model):
    date = models.DateField(unique=True)
    value = models.IntegerField() 

    class Meta:
        verbose_name = "Nonfarm Payroll Total People Employed"
        verbose_name_plural = "Nonfarm Payroll Total People Employed Data"
        ordering = ['-date']

    def __str__(self):
        return f"{self.date} - {self.value}"















# class IncomeStatementData(models.Model):
#     REPORT_TYPE_CHOICES = [
#         ('annual', 'Annual'),
#         ('quarterly', 'Quarterly'),
#     ]
#     stock = models.ForeignKey(
#         BaseStockData,
#         on_delete=models.CASCADE,
#         related_name='income_statement_data',
#         null=True,
#         )
#     report_type = models.CharField(max_length=9, choices=REPORT_TYPE_CHOICES)
#     date = models.DateField()

#     # Set null=True and blank=True for fields that can accept NULL values
#     gross_profit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
#     total_revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
#     cost_of_revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
#     cogs = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
#     operating_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
#     net_investment_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
#     net_interest_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
#     interest_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
#     interest_expense = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
#     non_interest_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
#     other_non_operating_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
#     depreciation = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
#     depreciation_amortization = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
#     income_before_tax = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
#     income_tax_expense = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
#     interest_and_debt_expense = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
#     net_income_from_continuing_operations = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
#     comprehensive_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
#     ebit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
#     ebitda = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
#     net_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

#     class Meta:
#         unique_together = ('stock', 'report_type', 'date')

#     def __str__(self):
#         return f"{self.symbol} - {self.date} - {self.report_type}"


# class BalanceSheetDataMeta(type(models.Model)):
#     def __new__(cls, name, bases, attrs):
#         balance_sheet_fields = [
#             'total_assets',
#             'total_current_assets',
#             'cash_and_cash_equivalents_at_carrying_value',
#             'cash_and_short_term_investments',
#             'inventory',
#             'current_net_receivables',
#             'total_non_current_assets',
#             'property_plant_equipment',
#             'accumulated_depreciation_amortization_ppe',
#             'intangible_assets',
#             'intangible_assets_excluding_goodwill',
#             'goodwill',
#             'investments',
#             'long_term_investments',
#             'short_term_investments',
#             'other_current_assets',
#             'other_non_current_assets',
#             'total_liabilities',
#             'total_current_liabilities',
#             'current_accounts_payable',
#             'deferred_revenue',
#             'current_debt',
#             'short_term_debt',
#             'total_non_current_liabilities',
#             'capital_lease_obligations',
#             'long_term_debt',
#             'current_long_term_debt',
#             'long_term_debt_noncurrent',
#             'short_long_term_debt_total',
#             'other_current_liabilities',
#             'other_non_current_liabilities',
#             'total_shareholder_equity',
#             'treasury_stock',
#             'retained_earnings',
#             'common_stock',
#             'common_stock_shares_outstanding'
#         ]
            
#         for field_name in balance_sheet_fields:
#             attrs[field_name] = StockIntegerField()

#         return super().__new__(cls, name, bases, attrs)
    
    
# class BalanceSheetData(models.Model):
#     REPORT_TYPE_CHOICES = [
#         ('annual', 'Annual'),
#         ('quarterly', 'Quarterly'),
#     ]
#     stock = models.ForeignKey(
#         BaseStockData,
#         on_delete=models.CASCADE,
#         related_name='balance_sheet_data',
#         null=True,
#         )
#     report_type = models.CharField(max_length=9, choices=REPORT_TYPE_CHOICES)
#     date = models.DateField()
        
#     class Meta:
#         unique_together = ('stock', 'report_type', 'date')

#     def __str__(self):
#         return f"{self.symbol} - {self.date} - {self.report_type}"