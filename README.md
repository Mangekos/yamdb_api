## API YAMDB.___
### Команда: Максим Белоногов(team lead), Квитковский Дмитрий, Максим Соловьев
Было не просто, но мы справились!

___
### REST API сервис.

___
Сервис для отзывов к произведениям.

### Внимание нельзя использовать ник -me- для регистрации
При запросе на users/me/ - вы попадете на страницу своего пользователя.

Спасибо за понимание.

С уважением, создатели проекта!

### Схема БД:
![Схема_БД](https://github.com/contdod1x/api_yamdb/blob/master/%D0%A1%D1%85%D0%B5%D0%BC%D0%B0_%D0%91%D0%94.jpg)

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/aafedotov/api_yamdb.git
```

```
api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
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

## Примеры запросов к API:

```angular2html
GET
http://127.0.0.1:8000/api/v1/titles/

Получение списка всех произведений
```

```angular2html
GET
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/

Получение списка отзывов к произведению
```

```angular2html
POST
http://127.0.0.1:8000/api/v1/auth/signup/

Регистрация пользователей, получение кода подтверждения на e-mail
```

### Подробная информация по Api в ReDoc.

## Импорт данных из CSV:
Данные для импорта хранить в папке api_yamdb\static\data
Просим вас внимательно предоставлять данные для импорта
не допускайте ошибки в названии колонок в файлах

Команда для из CSV

```
python manage.py import_data
```
