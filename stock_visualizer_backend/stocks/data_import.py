from django.core.management.base import BaseCommand, CommandError
from stocks.models import StockData
import csv

class Command(BaseCommand):
  help = 'Import stock data from a CSV file'

  def add_arguments(self, parser):
    parser.add_argument('csv_file', type=str, help='Path to the CSV file containing stock data')

  def handle(self, *args, **options):
    file_path = options['csv_file']
    try:
      with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
          StockData.objects.create(
            symbol=row['symbol'],
            date=row['date'],
            open_price=row['open'],
            high_price=row['high'],
            low_price=row['low'],
            close_price=row['close'],
            adjusted_close_price=row['adj_close'],
            volume=row['volume'],
            dividend=row['dividend'],
          )
      self.stdout.write(self.style.SUCCESS('Successfully imported stock data'))
    except Exception as e:
      raise CommandError(f'Error importing stock data: {e}')
