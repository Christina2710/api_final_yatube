# API Final Project

Этот проект представляет собой REST API для платформы блогов, позволяющий пользователям взаимодействовать с контентом и друг с другом. Пользователи могут создавать, редактировать и удалять свои записи, комментировать публикации других пользователей и подписываться на интересных авторов.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Christina2710/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```
### Некоторые примеры запросов к API

*POST /api/v1/follow/

```
{
"following": "string"
}
```
Пример ответа:
```
{
"user": "string",
"following": "string"
}
```
