from django.db import models

class StockDecimalField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        # Set default values for max_digits and decimal_places
        kwargs.setdefault('max_digits', 15)
        kwargs.setdefault('decimal_places', 2)
        kwargs.setdefault('null', True)
        kwargs.setdefault('blank', True)
        super().__init__(*args, **kwargs)
        
class BaseStockData(models.Model):
    SECTOR_CHOICES = [
        ('Industrials', 'Industrials'),
        ('Financials', 'Financials'),
        ('Information Technology', 'Information Technology'),
        ('Health Care', 'Health Care'),
        ('Consumer Discretionary', 'Consumer Discretionary'),
        ('Consumer Staples', 'Consumer Staples'),
        ('Real Estate', 'Real Estate'),
        ('Utilities', 'Utilities'),
        ('Materials', 'Materials'),
        ('Energy', 'Energy'),
        ('Communication Services', 'Communication Services'),
    ]
    symbol = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    sector = models.CharField(max_length=25, choices=SECTOR_CHOICES)
    headquarters = models.CharField(max_length=255)
    date_added = models.DateField()

    def __str__(self):
        return f"{self.symbol} - {self.name}"
    
    
class MonthlyStockPriceData(models.Model):
    stock = models.ForeignKey(
        BaseStockData,
        on_delete=models.CASCADE,
        related_name='monthly_price_data',
        null=True,
        )
    date = models.DateField()
    open = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    adj_close = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()
    dividend = models.DecimalField(max_digits=10, decimal_places=2)  
    class Meta:
        unique_together = ('stock', 'date')

    def __str__(self):
        return f"{self.stock.symbol} - {self.date}"
        

# We are going to use this metaclass to construct the IncomeStatementData and BalanceSheetData classes
class FinancialDataMeta(type(models.Model)):
    def __new__(cls, name, bases, attrs):
        # Check if the class has a 'financial_fields' attribute
        financial_fields = attrs.pop('financial_fields', [])
        
        for field_name in financial_fields:
            attrs[field_name] = StockDecimalField()
        
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
