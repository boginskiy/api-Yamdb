# API базы отзывов «Yamdb»

### **Описание проекта**
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха.
Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

### **Использованные технологии**
* Django 2.2.16
* pytest 6.2.4
* pytest-pythonpath 0.7.3
* pytest-django 4.4.0
* djangorestframework 3.12.4
* djangorestframework-simplejwt 4.7.2
* django-filter 2.4.0
* PyJWT 2.1.0
* requests 2.26.0

### **Запускаем проект в dev режиме (OC Linux)**
Клонировать репозиторий с GitHub
```
git clone git@github.com:boginskiy/api-Yamdb.git
```

Установить виртуальное окружение venv
```
python3 -m venv venv
```

Aктивировать виртуальное окружение venv
```
source venv/bin/activate
```

Обновить менеджер пакетов pip
```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt
```
pip install -r requirements.txt
```

Выполнить миграции
```
python3 manage.py migrate
```

Создание суперпользователя
```
python3 manage.py createsuperuser
```

Запустить проект
```
python3 manage.py runserver
```

### **Примеры запросов API**
### **Запросы к AUTH (Регистрация пользователей и выдача токенов):**
Регистрация нового пользователя. (POST): `http://127.0.0.1:8000/api/v1/auth/signup/`

```
    {
        "email": "string",
        "username": "string"
    }
```

* _Использовать имя 'me' в качестве username запрещено_
* _Доступно любому пользователю_
---

###### Запрос к AUTH
Получение JWT-токена. (POST): `http://127.0.0.1:8000/api/v1/auth/token/`

```
    {
        "username": "string"
        "confirmation_code": "string"
    }
```
* _confirmation_code - при регистрации нового пользователя в директории проекта **api_yamdb/sent_emails** появляется файл.log в котором находится данный код_
* _Доступно любому пользователю_
---

### **Запросы для произведений (title)**
Получить спискок публикаций (GET): `http://127.0.0.1:8000/api/v1/titles/`

* _При запросах доступны параметры:_
_category - фильтрует по полю slug категории (тип string);_
_genre - фильтрует по полю slug жанра (тип string);_
_name - фильтрует по названию произведения (тип string);_
_year - фильтрует по году (тип integer);_

* _Допустимы анонимные запросы от пользователей_
---

###### Запрос к title
Добавление произведения (POST): `http://127.0.0.1:8000/api/v1/titles/`

```
    {
        "name": "string",
        "year": "integer",
        "description": "string",
        "genre": "Array of strings (Slug жанра)",
        "category": "string (Slug категории)"
    }
```

* _Добавить произведение может только администратор_
* _Нельзя добавлять произведения, которые еще не вышли (год выпуска не может быть больше текущего)_
* _При добавлении нового произведения требуется указать уже существующие категорию и жанр_
---

###### Запрос к title
Получить публикацию (GET): `http://127.0.0.1:8000/api/v1/titles/{titles_id}/`

* _{titles_id} - id произведения_
* _Допустимы анонимные запросы от пользователей_
---

###### Запрос к title
Частичное обновление информации о произведении (PUTCH): `http://127.0.0.1:8000/api/v1/titles/{titles_id}/`

```
    {
        "name": "string",
        "year": 0,
        "description": "string",
        "genre": [
            "string"
        ],
        "category": "string"
    }
```

* _{titles_id} - id произведения_
* _Обновить произведение может только администратор_
---

###### Запрос к title
Удаление произведения (DELETE): `http://127.0.0.1:8000/api/v1/titles/{titles_id}/`

* _{titles_id} - id произведения_
* _Удалить произведение может только администратор_
---

### **Запросы к отзывам на произведения (reviews):**
Получение всех отзывов к произведению (GET): `http://127.0.0.1:8000/api/v1/titles/{titles_id}/reviews/`

* _{titles_id} - id произведение с отзывом_
* _Допустимы анонимные запросы от пользователей_
---

###### Запрос к reviews
Добавление нового отзыва к произведению (POST): `http://127.0.0.1:8000/api/v1/titles/{titles_id}/reviews/`

```
    {
        "text": "string",
        "score": 10
    }
```

* _{titles_id} - id произведение с отзывом_
* _Поле "score" устанавливается от 1 до 10_
* _Добавить отзыв к произведению может только авторизованный пользователь и только один раз_
---

###### Запрос к reviews
Получение отзыва к произведению по id (GET): `http://127.0.0.1:8000/api/v1/titles/{titles_id}/reviews/{reviews_id}/`

* _{titles_id} - id произведение с отзывом_
* _{reviews_id} - id отзыва_
* _Допустимы анонимные запросы от пользователей_
---

###### Запрос к reviews
Частичное обновление отзыва к произведению по id (PUTCH): `http://127.0.0.1:8000/api/v1/titles/{titles_id}/reviews/{reviews_id}/`

```
    {
        "text": "string",
        "score": 8
    }
```

* _{titles_id} - id произведение с отзывом_
* _{reviews_id} - id отзыва_
* _Поле "score" устанавливается от 1 до 10_
* _Обновить отзыв может автор, модератор или администратор_
---

###### Запрос к reviews
Удаление отзыва к произведению по id (DELETE): `http://127.0.0.1:8000/api/v1/titles/{titles_id}/reviews/{reviews_id}/`

* _{titles_id} - id произведение с отзывом_
* _{reviews_id} - id отзыва_
* _Удалить отзыв может автор, модератор или администратор_
---

### **Запросы к комментариям отзывов к произведениям (comments):**
Получение списка всех комментариев к отзыву. (GET): `http://127.0.0.1:8000/api/v1/titles/{titles_id}/reviews/{reviews_id}/comments/`

* _{titles_id} - id произведение с отзывом_
* _{reviews_id} - id отзыва_
* _Допустимы анонимные запросы от пользователей_
---

###### Запрос к comments
Добавить новый комментарий для отзыва по id. (POST): `http://127.0.0.1:8000/api/v1/titles/{titles_id}/reviews/{reviews_id}/comments/`

```
    {
        "text": "string"
    }
```

* _{titles_id} - id произведение с отзывом_
* _{reviews_id} - id отзыва_
* _Добавить комментарий к отзыву может только авторизованный пользователь неограниченное кол-во раз_
---

###### Запрос к comments
Получить комментарий для отзыва по id. (GET): `http://127.0.0.1:8000/api/v1/titles/{titles_id}/reviews/{reviews_id}/comments/{comment_id}/`

* _{titles_id} - id произведение с отзывом_
* _{reviews_id} - id отзыва_
* _{comment_id} - id комментария_
* _Допустимы анонимные запросы от пользователей_
---

###### Запрос к comments
Частичное обновление комментария к отзыву. (PATCH): `http://127.0.0.1:8000/api/v1/titles/{titles_id}/reviews/{reviews_id}/comments/{comment_id}/`

```
    {
        "text": "string"
    }
```

* _{titles_id} - id произведение с отзывом_
* _{reviews_id} - id отзыва_
* _{comment_id} - id комментария_
* _Обновить комментарий может автор, модератор или администратор_
---

###### Запрос к comments
Удаление комментария к отзыву по id (DELETE): `http://127.0.0.1:8000/api/v1/titles/{titles_id}/reviews/{reviews_id}/comments/{comment_id}/`

* _{titles_id} - id произведение с отзывом_
* _{reviews_id} - id отзыва_
* _{comment_id} - id комментария_
* _Удалить комментарий может автор, модератор или администратор_
---

### **Запросы к пользователям (users):**
Получение списка всех пользователей. (GET): `http://127.0.0.1:8000/api/v1/users/`

* _При запросах доступны параметры:_
_search - поиск по имени пользователя (username) (тип string);_
* _Доступно только администратору_
---

###### Запрос к users
Добавление пользователя. (POST): `http://127.0.0.1:8000/api/v1/users/`

```
    {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
    }
```

* _Поля email и username должны быть уникальными_
* _Доступно только администратору_
---

###### Запрос к users
Получение пользователя по username. (GET): `http://127.0.0.1:8000/api/v1/users/{username}`

* _{username} - Username пользователя_
* _Доступно только администратору_
---

###### Запрос к users
Изменение данных пользователя по username. (PATCH): `http://127.0.0.1:8000/api/v1/users/{username}`

```
    {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
    }
```

* _Поля email и username должны быть уникальными_
* _Доступно только администратору_
---

###### Запрос к users
Удаление пользователя по username. (DELETE): `http://127.0.0.1:8000/api/v1/users/{username}`

* _Доступно только администратору_
---

### **Запросы к учетным данным пользователя (users/me):**
Получение данных своей учетной записи. (GET): `http://127.0.0.1:8000/api/v1/users/me/`

* _Доступно любому авторизованному пользователю_
---

###### Запрос к users/me
Изменение данных своей учетной записи. (PATCH): `http://127.0.0.1:8000/api/v1/users/me/`

```
    {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
    }
```

* _Поля email и username должны быть уникальными_
* _Доступно любому авторизованному пользователю_
---

### **Авторы**
[Одоевская Мария](https://github.com/MariaOdoevskaya) - python разработчик

[Березин Владимир](https://github.com/barki90) - python разработчик

[Богинский Дмитрий](https://github.com/boginskiy) - python разработчик, тимлид команды
