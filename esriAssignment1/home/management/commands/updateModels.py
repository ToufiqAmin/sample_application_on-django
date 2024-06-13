from typing import Any
from django.core.management.base import BaseCommand, CommandParser
import pandas as pd

class Command(BaseCommand):
    help = 'import booms'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        return super().handle(*args, **options)