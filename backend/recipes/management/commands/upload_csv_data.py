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
            uploaded_ingredients_count = 0
            discarded_ingredients_count = 0
            print("Загружаем ингредиенты в базу данных...")
            for row in csv_reader:
                try:
                    Ingredient.objects.create(
                        name=row[0].lower(), unit=row[1].lower()
                    )
                    uploaded_ingredients_count += 1

                except Exception:
                    print(
                        f"Ингредиент '{row[0]}' уже есть в базе данных или не соответствует формату"
                    )
                    discarded_ingredients_count += 1
            print(
                f"Добавление ингредиентов завершено.\n  - ингредиентов добавлено: {uploaded_ingredients_count}\n  - ингредиентов отклонено (как дубликаты или не соответствующие формату): {discarded_ingredients_count}"
            )
