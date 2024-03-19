from django.db import models

# Create your models here.

class StockData(models.Model):
    symbol = models.CharField(max_length=20)
    date = models.DateField()
    open = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    adj_close = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()
    dividend = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.symbol} - {self.date}"


class IncomeStatementData(models.Model):
    symbol = models.CharField(max_length=20)
    report_type = models.CharField(max_length=10)
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

    def __str__(self):
        return f"{self.symbol} - {self.date} - {self.report_type}"

