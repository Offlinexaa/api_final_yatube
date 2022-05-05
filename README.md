# yatube api

REST API для социальной cети yatube. Программный интерфейс предназначенный для управления сетью без применения web-браузера.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Offlinexaa/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip setuptools
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Документация доступна по ссылке:

```
http://127.0.0.1:8000/redoc/
```

### Требования

Python 3.7 и выше

Django framework 2.2.16

Django Rest framework 3.12.4

Django Rest framework simplejwt 4.7.2

Pillow 8.3.1

PyJWT 2.1.0

requests 2.26.0

djoser
