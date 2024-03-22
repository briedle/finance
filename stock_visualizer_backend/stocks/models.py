# models.py

from django.db import models

# Create your models here.

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
        return f"{self.symbol} - {self.date}"


class IncomeStatementData(models.Model):
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

    # Set null=True and blank=True for fields that can accept NULL values
    gross_profit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    cost_of_revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    cogs = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    operating_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    net_investment_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    net_interest_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    interest_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    interest_expense = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    non_interest_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    other_non_operating_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    depreciation = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    depreciation_amortization = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    income_before_tax = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    income_tax_expense = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    interest_and_debt_expense = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    net_income_from_continuing_operations = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    comprehensive_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    ebit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    ebitda = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    net_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('stock', 'report_type', 'date')

    def __str__(self):
        return f"{self.symbol} - {self.date} - {self.report_type}"

