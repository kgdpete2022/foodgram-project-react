import csv, os
from pathlib import Path
from django.core.management.base import BaseCommand
from foodgram.settings import BASE_DIR
from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(
            os.path.join(BASE_DIR.parent / "data/ingredients.csv"),
            encoding="utf-8",
        ) as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                try:
                    print(row)
                    Ingredient.objects.create(name=row[0], unit=row[1])
                except IntegrityError:
                    print(row)
