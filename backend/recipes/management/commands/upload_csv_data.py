import csv
import os
from pathlib import Path
import json

from django.core.management.base import BaseCommand

from django.contrib.auth import get_user_model

from recipes.models import Ingredient, Tag

User = get_user_model()


DATA_DIR_PATH = (
    f"{Path(__file__).resolve().parent.parent.parent.parent.parent}/data/"
)


class Command(BaseCommand):

    MODELS = {
        "tags": Tag.objects.create(
            name="temp",
            color="temp",
            slug="temp"
        ),
        "ingredients": Ingredient.objects.create(
            name="temp",
            measurement_unit="temp"
        ),
        "users": User.objects.create(
            username="temp",
            first_name="temp",
            last_name="temp",
            email="temp@email.com",
            password="tempPass,0000",
        ),
    }

    def handle(self, *args, **options):
        filenames = self.get_datafile_names(DATA_DIR_PATH)

    def get_datafile_names(self, full_path):
        valid_names = []
        for dirpath, dirnames, filenames in os.walk(full_path):
            for filename in filenames:
                if filename[-5:] == ".json" and filename[:-5] in MODELS:
                    valid_names.append(filename)
        return valid_names
    
    def upload_tags(self, tags):
        print(f"--------------------------------------------------------------")
        print("Загружаем теги в базу данных...")
        uploaded = 0
        discarded = 0
        for tag in tags:
            try:
                Tag.objects.create(
                    name=tag["name"].lower(),
                    color=tag["color"].lower(),
                    slug=tag["slug"].lower()
                )
            except Exception as e:
                print(f"Teг {tag} уже есть в базе данных или не соответствует формату ({e})")
        print(
            f"Добавление тегов завершено.\n"
            f"- тегов добавлено: {uploaded}\n"
            f"- тегов отклонено "
            f"(как дубликаты или не соответствующие формату): "
            f"{discarded}"
            )
        
    def upload_ingredients(self, ingredients):
        print("--------------------------------------------------------------")
        print("Загружаем ингредиенты в базу данных...")
        uploaded = 0
        discarded = 0
        for ingredient in ingredients:
            try:
                Tag.objects.create(
                    name=ingredient["name"].lower(),
                    measurement_unit=ingredient["measurement_unit"].lower(),
                )
            except Exception as e:
                print(f"Игредиент {ingredient} уже есть в базе данных или не соответствует формату ({e})")
        print(
            f"Добавление ингредиентов завершено.\n"
            f"- ингредиентов добавлено: {uploaded}\n"
            f"- ингредиентов отклонено "
            f"(как дубликаты или не соответствующие формату): "
            f"{discarded}"
            )
        
    def upload_users(self, users):
        print("--------------------------------------------------------------")
        print("Загружаем пользователей в базу данных...")
        uploaded = 0
        discarded = 0
        for user in users:
            try:
                Tag.objects.create(
                    username=user["username"],
                    first_name=user["first_name"].capitalize(),
                    last_name=user["last_name"].capitalize(),
                    email=user["email"],
                    password=user["password"],                    
                )
            except Exception as e:
                print(f"Пользователь {user} уже есть в базе данных или не соответствует формату ({e})")
        print(
            f"Добавление пользователей завершено.\n"
            f"- пользователей добавлено: {uploaded}\n"
            f"- пользователей отклонено "
            f"(как дубликаты или не соответствующие формату): "
            f"{discarded}"
            )        


    def read_data(self, filename):
        with open(f"{filename}.json") as f:
            rawdata = json.load(f)
            dump = json.dumps(rawdata)
            if filename == "tags":




dump = json.dumps(data)
