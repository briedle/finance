from django.core.management.base import BaseCommand
from stocks.utils import parse_alpha_vantage as pav

class Command(BaseCommand):
    help = 'Sync various economic indicators data'

    def handle(self, *args, **options):
        pav.sync_economic_indicators()
