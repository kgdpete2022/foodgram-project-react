# Cайт Foodgram - «Продуктовый помощник» (онлайн-сервис + API)
Пользователи сайта могут:
- публиковать рецепты
- подписываться на публикации других пользователей
- добавлять понравившиеся рецепты в список «Избранное» и «Список покупок»
- скачивать в виде файла сводный список продуктов, необходимых для приготовления выбранных блюд


Проект доступен по адресу http://51.250.20.57/

Данные для входа под тестовыми пользоватлеями: 

Email:
ivanov@gmail.com
petrov@gmail.com
sidorov@gmail.com
admin@gmail.com

Пароль (общий для всех):
foNOVYIparol,2022


## Порядок установки на локальный компьютер

1. Установите Docker и Docker Compose для работы с образами:
Windows: 
Установите приложение Docker Desktop - https://www.docker.com/products/docker-desktop/

Linux:
```bash
sudo apt install docker.io
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

2. Клонируйте репозиторий на локальный компьютер:
'''
git@github.com:kgdpete2022/foodgram-project-react.git
'''

3. Создайте в папке /infra файл .env и наполните его своими данными (для работы с PostgreSQL):

Шаблон для заполнения файла ".env":
```python
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY='Ваш секретный ключ'
ALLOWED_HOSTS=127.0.0.1
```

* - Для генерации секретного ключа (SECRET_KEY): 
'''bash
python manage.py shell
from django.core.management.utils import get_random_secret_key
get_random_secret_key()
'''

4. Перейдите папку /frontend создайте образ фронтенда:
'''bash
docker build -t kgdpete/foodgram_frontend .
'''

5. Перейдите папку /backend создайте образ бэкенда:
'''bash
docker build -t kgdpete/foodgram_backend .
'''

6. Перейдите папку /infra и запустите Docker Compose для создания образов postgres и nginx, и запуска контейнеров из образов:
'''bash
docker-compose up -d
'''

7. Произведите миграции в БД:
'''bash
docker-compose exec backend python manage.py migrate
'''

- (По желанию) Добавьте в БД ранее созданные данные:
'''bash
docker-compose exec backend python manage.py loaddata fixtures.json
'''

8. Соберите статику:
'''bash
docker-compose exec backend python manage.py collectstatic --no-input
'''

9. Создайте суперпользователя:
'''bash
docker-compose exec backend python manage.py createsuperuser
'''

Сайт доступен по адресу: localhost.
Админ-панель сайта: http://localhost/admin (используйте логин и пароль созданного суперпользователя)


## Техническая информация

Стек технологий: Python, Django, Django REST framework, PostgreSQL, React

Веб-сервер: nginx (контейнер nginx)  
Frontend фреймворк: React (контейнер frontend)  
Backend фреймворк: Django (контейнер backend)  
API фреймворк: Django REST (контейнер backend)  
База данных: PostgreSQL (контейнер db)

## Создание бэкенда
Петр Шопин (mail4dev2022@gmail.com)

