import csv
import os

from django.core.management.base import BaseCommand

from foodgram.settings import BASE_DIR

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open("../../data/ingredients.csv",
            encoding="utf-8",
        ) as csv_file:
            csv_reader = csv.reader(csv_file)
            uploaded_ingredients_count = 0
            discarded_ingredients_count = 0
            print("Загружаем ингредиенты в базу данных...")
            for row in csv_reader:
                try:
                    Ingredient.objects.create(
                        name=row[0].lower(), measurement_unit=row[1].lower()
                    )
                    uploaded_ingredients_count += 1

                except Exception:
                    print(
                        f"Ингредиент '{row[0]}' уже есть в базе данных"
                        f"или не соответствует формату."
                    )
                    discarded_ingredients_count += 1
            print(
                f"Добавление ингредиентов завершено.\n"
                f"- ингредиентов добавлено: {uploaded_ingredients_count}\n"
                f"- ингредиентов отклонено "
                f"(как дубликаты или не соответствующие формату): "
                f"{discarded_ingredients_count}"
            )
