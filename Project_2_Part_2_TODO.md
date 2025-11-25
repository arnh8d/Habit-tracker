# Проект 2. Часть 2: HTML-интерфейс и расширенный API

## Описание задачи

Расширь проект из Части 1, добавив полнофункциональный HTML-интерфейс и полный набор CRUD-операций для управления привычками.

**Предварительное условие:** Выполнена Часть 1

## Цель

Освоить навыки интеграции веб-интерфейса с бэкендом на Python (FastAPI, Jinja2), расширить функциональность REST API до полного набора CRUD-операций, закрепить принципы организации бизнес-логики.

## Структура проекта

### ВАЖНО! Строго придерживайся этой структуры для прохождения автотестов!

```
project_root/
├── habit_tracker/                      # Основной пакет
│   ├── __init__.py
│   │
│   ├── api/                            # API роуты (JSON)
│   │   ├── __init__.py
│   │   └── habits_api.py               # ПЕРЕИМЕНОВАНО с habits.py!
│   │
│   ├── core/                           # Бизнес-логика
│   │   ├── __init__.py
│   │   ├── models.py                   # Расширены модели
│   │   └── services.py                 # Добавлены CRUD функции
│   │
│   ├── views/                          # НОВАЯ папка для веб-роутов
│   │   ├── __init__.py
│   │   └── web.py                      # HTML-страницы
│   │
│   ├── templates/                      # НОВАЯ папка для HTML-шаблонов
│   │   ├── index.html                  # Главная страница
│   │   └── habit_detail.html           # Детальная страница
│   │
│   ├── static/                         # НОВАЯ папка для статики
│   │   ├── css/
│   │   │   └── style.css               # Стили
│   │   └── js/
│   │       └── script.js               # JavaScript
│   │
│   └── main.py                         # Обновлён (подключена статика)
│
├── requirements.txt                    # Обновлён (добавлены jinja2, python-multipart)
└── README.md                           # Обновлён (добавлено описание веб-интерфейса)
```

## Изменения относительно Части 1

### 1. Переименование API-файла

Файл с API для привычек должен называться `habit_tracker/api/habits_api.py` (в Части 1 он был `habits.py`).

### 2. Дополнительные папки и файлы проекта

Проект во второй части должен содержать дополнительные папки и файлы для веб-интерфейса:

```bash
# Папки
habit_tracker/views
habit_tracker/templates
habit_tracker/static/css
habit_tracker/static/js

# Файлы
habit_tracker/views/__init__.py
habit_tracker/views/web.py
habit_tracker/templates/index.html
habit_tracker/templates/habit_detail.html
habit_tracker/static/css/style.css
habit_tracker/static/js/script.js
```

Код для файлов HTML-шаблонов, CSS и JS находятся в ниже в этом задании.  
Твоя задача — **подключить и интегрировать** их в проект (править фронтенд-код не обязательно, достаточно сохранить требуемые идентификаторы и поведение).

## Требования к реализации

### 1. Файл `habit_tracker/main.py`

**Задача:** Обнови `main.py` так, чтобы приложение:

- продолжало предоставлять JSON API для привычек;
- обслуживало статические файлы из `habit_tracker/static`;
- подключало роуты веб-интерфейса (HTML-страницы) и JSON API.

**Что нужно сделать:**

1. Импортировать необходимые модули:
   - `StaticFiles` из `fastapi.staticfiles` для обслуживания статики
   - `habits_api` из `habit_tracker.api` (переименованный модуль)
   - `web` из `habit_tracker.views` (новый модуль)

2. Подключить статические файлы:
   ```python
   app.mount("/static", StaticFiles(directory="habit_tracker/static"), name="static")
   ```
   Это позволит обращаться к CSS и JS по путям `/static/css/style.css` и `/static/js/script.js`.

3. Подключить роутеры:
   - Роутер веб-интерфейса: `app.include_router(web.router, tags=["Web Interface"])`
   - Роутер API с префиксом: `app.include_router(habits_api.router, prefix="/api/habits", tags=["Habits API"])`


### 2. Файл `habit_tracker/core/models.py`

**Задача:** Добавь поле `streak` и новые модели

#### 2.1. Обновление внутреннего класса Habit

- Добавь поле `self.streak: int = 0` в `__init__` класса `Habit`

#### 2.2. Новые Pydantic модели

**`HabitUpdate`** - для обновления привычки
- Поле `name: str` с валидацией (не должно быть пустым)

**`HabitBase`** - базовая модель для ответов API
- Поля: `id: int`, `name: str`
- Используется как базовый класс для других response-моделей

**`HabitResponse`** - полная информация о привычке (наследуется от `HabitBase`)
- Дополнительные поля: `marks: list[date]`, `streak: int`
- Используется для `GET /api/habits/{id}/` и `GET /api/habits/`

**`HabitDetailResponse`** - детальная информация (опционально, можно использовать `HabitResponse`)
- Поля: `id`, `name`, `marks` (List[str] или List[date]), `streak`

#### 2.3. Обновить существующие модели

- В `HabitMarkResponse` добавь поле `streak: int`
- В `HabitListResponse` добавь поле `streak: int` (или используй `HabitResponse` для списка)

### 3. Файл `habit_tracker/core/services.py`

Здесь находится основная бизнес-логика работы с привычками во второй части проекта.  
Ты свободен в деталях реализации, но внешний интерфейс и поведение должны соответствовать требованиям ниже.

#### 3.1. Константа TODAY и хранилище

- Используется фиксированная дата `TODAY = date(2025, 7, 12)` для предсказуемости работы приложения.
- В памяти хранится база привычек: `habits_db: dict[int, Habit]` и счётчик `next_habit_id`.

Это тот же in‑memory подход, что и в Части 1, но теперь им управляет сервисный слой.

#### 3.2. Функции бизнес-логики

В этом модуле должны быть реализованы функции для работы с привычками. Все функции работают с глобальными переменными `habits_db` и `next_habit_id`.

**Обязательные функции и их смысл:**

- `calculate_streak(marks: list[date]) -> int`  
  Рассчитывает *текущий* streak по датам в `marks` относительно `TODAY`.  
  Алгоритм в общих чертах:
  - пустой список -> streak = 0;
  - работай с отсортированным по убыванию набором уникальных дат;
  - если среди последних дат нет ни `TODAY`, ни вчерашнего дня -> streak = 0;
  - иначе отсчитывай подряд идущие дни назад (без пропусков) от `TODAY` или вчерашнего дня.

- `get_all_habits_with_details() -> list[dict]`  
  Возвращает список привычек, где для каждой привычки в словаре есть все её поля (`id`, `name`, `marks` как список дат) **и** рассчитанный `streak`.  
  Список должен быть отсортирован по `id` (по возрастанию).  
  **Важно:** `marks` должен быть списком объектов `date`, так как в шаблонах может использоваться форматирование дат.

- `get_habit_by_id_with_details(habit_id: int) -> dict | None`  
  Возвращает одну привычку по `id` в виде словаря с полями привычки (включая `id`, `name`, `marks` как список дат) и рассчитанным `streak`, либо `None`, если привычки нет.  
  **Важно:** `marks` должен быть списком объектов `date`, а не строк, так как в шаблонах используется `mark.strftime()`.

- `create_habit(habit_data: HabitCreate) -> Habit`  
  Создаёт новую привычку:
  - имя не должно быть пустым (валидация на уровне сервиса; при ошибке выбрасывается `ValueError`);
  - имя должно быть уникальным среди существующих привычек;
  - используется и увеличивается глобальная переменная `next_habit_id` (используй `global next_habit_id`).

- `update_habit(habit_id: int, habit_data: HabitUpdate) -> Habit | None`  
  Обновляет существующую привычку:
  - возвращает обновлённую привычку или `None`, если она не найдена;
  - проверяет непустое имя и уникальность нового имени (ошибки — через `ValueError`).

- `delete_habit(habit_id: int) -> bool`  
  Удаляет привычку из `habits_db` и возвращает `True` при успехе, `False`, если такой привычки нет.

- `mark_habit(habit_id: int) -> dict | None`  
  Отмечает привычку за `TODAY`:
  - при отсутствии привычки возвращает `None`;
  - при повторной отметке за `TODAY` выбрасывает `ValueError`;
  - добавляет дату в `marks` и возвращает словарь с `id`, `name`, `last_marked_at` и актуальным `streak`.

- `is_habit_marked_today(habit_id: int) -> bool`  
  Отвечает, отмечена ли привычка за `TODAY` (используется во вьюхах для отображения кнопки/чекбокса).

#### 3.3. Предзаполненные данные (опционально)

Для демонстрации можно предзаполнить `habits_db`:
```python
habits_db: dict[int, Habit] = {
    1: Habit(id=1, name="Бег", marks=[date(2025, 7, 10), date(2025, 7, 11)]),
    2: Habit(id=2, name="Чтение", marks=[date(2025, 7, 11)]),
    3: Habit(id=3, name="Медитация", marks=[])
}
next_habit_id = 4
```

### 4. Файл `habit_tracker/api/habits_api.py`

JSON API-слой, который использует функции из `services` и предоставляет REST-интерфейс для фронтенда.

#### 4.1. Общие требования

- Роутер должен находиться в модуле `habit_tracker/api/habits_api.py` и подключаться в `main.py` с префиксом `/api/habits`.
- Внутри модуля импортируй функции из `habit_tracker.core.services` (например, `from habit_tracker.core.services import create_habit, get_all_habits_with_details, ...`).
- При ошибках валидации/бизнес-логики (`ValueError` из функций сервиса) нужно возвращать HTTP 400 с текстом ошибки.

#### 4.2. Обязательные эндпоинты

С учётом префикса `/api/habits` роутер должен предоставлять следующее API:

- `POST /api/habits/` — создание привычки  
  - Request body: `HabitCreate`  
  - Response: `HabitBase` (`id`, `name`)  
  - Status: `201 Created`

- `GET /api/habits/` — список всех привычек  
  - Response: `list[HabitResponse]` (включая `streak`)  
  - Status: `200 OK`

- `GET /api/habits/{id}/` — получение одной привычки  
  - Response: `HabitResponse`  
  - Status: `200 OK` или `404 Not Found`, если привычки нет

- `PUT /api/habits/{id}/` — обновление привычки  
  - Request body: `HabitUpdate`  
  - Response: `HabitBase`  
  - Status: `200 OK` / `400 Bad Request` / `404 Not Found`

- `DELETE /api/habits/{id}/` — удаление привычки  
  - Response body не обязателен  
  - Status: `204 No Content` или `404 Not Found`

- `POST /api/habits/{id}/mark/` — отметка выполнения  
  - Response: `HabitMarkResponse` (включая `streak`)  
  - Status: `200 OK` / `400 Bad Request` (повторная отметка) / `404 Not Found`

Точный вид кода обработчиков ты выбираешь сам — главное, чтобы они:
- вызывали функции из `services` с корректными аргументами;
- правильно переводили исключения сервиса в `HTTPException`;
- возвращали данные в формате, совместимом с описанными Pydantic‑моделями.

### 5. Файл `habit_tracker/views/web.py`

HTTP-роуты, которые рендерят HTML‑страницы на основе Jinja2‑шаблонов и обращаются к функциям из `services`.

#### 5.1. Общие требования

- Модуль `habit_tracker/views/web.py` должен объявлять роутер `router`.
- Для рендеринга HTML используется `Jinja2Templates` с директорией `habit_tracker/templates`.
- Для операций с привычками импортируй функции из `habit_tracker.core.services` (например, `from habit_tracker.core.services import get_all_habits_with_details, is_habit_marked_today, ...`).

#### 5.2. Обязательные маршруты

- `GET /` (`name="main-page"`) — главная страница  
  - Получает список всех привычек с деталями через `get_all_habits_with_details()`.  
  - Передаёт в шаблон `index.html`:
    - `habits` — список привычек (словари с полями `id`, `name`, `marks`, `streak`)
    - `is_marked_today` — функцию для проверки, отмечена ли привычка сегодня (передаётся как `is_habit_marked_today`, используется в шаблоне как `is_marked_today(habit.id)`)
  - Возвращает `TemplateResponse` с контекстом:
    ```python
    {
        "request": request, 
        "habits": habits, 
        "is_marked_today": is_habit_marked_today
    }
    ```
  - **Важно:** В шаблоне `index.html` используется `{% if not is_marked_today(habit.id) %}`, поэтому нужно передать функцию `is_habit_marked_today` в контекст шаблона.

- `GET /habit/{habit_id}/` (`name="habit-detail"`) — детальная страница привычки  
  - Получает привычку через `get_habit_by_id_with_details(habit_id)`.  
  - Если привычка не найдена (`None`) — выбрасывает `HTTPException(404)`.  
  - В шаблон `habit_detail.html` передаётся словарь/объект привычки с полями `id`, `name`, `marks` (список дат), `streak`.

- `POST /habit/add` (`name="add_habit_from_form"`) — добавление привычки из формы  
  - Читает поле `name` из формы через `Form(...)`.  
  - Создаёт `HabitCreate(name=name)` и вызывает `create_habit()`.  
  - При ошибках валидации (`ValueError`) можно обработать или просто редиректить (в тестах проверяется только редирект).  
  - После успешного создания делает редирект на главную через `RedirectResponse(url=router.url_path_for("main-page"), status_code=303)`.

- `POST /habit/{habit_id}/mark` (`name="mark_habit_from_form"`) — отметка привычки из формы  
  - Вызывает `mark_habit(habit_id)`.  
  - При ошибках (`ValueError` при повторной отметке) можно обработать или просто редиректить.  
  - Редиректит на главную через `router.url_path_for("main-page")`.

- `POST /habit/{habit_id}/edit` (`name="edit_habit_from_form"`) — редактирование названия  
  - Читает `name` из формы, создаёт `HabitUpdate(name=name)`, вызывает `update_habit()`.  
  - После успешного обновления перенаправляет на детальную страницу через `router.url_path_for("habit-detail", habit_id=habit_id)`.

- `POST /habit/{habit_id}/delete` (`name="delete_habit_from_form"`) — удаление привычки  
  - Вызывает `delete_habit(habit_id)`.  
  - Редиректит на главную страницу.

Конкретные сигнатуры обработчиков и способ передачи данных в шаблоны ты можешь выбрать сам, если:
- пути маршрутов и их HTTP‑методы совпадают с указанными;
- указанные `name` маршрутов используются там, где это важно (например, при построении URL в шаблонах);
- формы и кнопки из готовых шаблонов работают без изменений JS‑кода.

### 6. Шаблоны HTML

**Задача:** Интегрируй готовые HTML-шаблоны с использованием Jinja2

#### 6.1. Файл `habit_tracker/templates/index.html`

Создай файл `index.html` со следующим содержимым: 

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Трекер привычек</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <div class="container">
        <h1>Мои привычки</h1>

        <div class="habit-list">
            {% if habits %}
                {% for habit in habits %}
                <div class="habit-item">
                    <div class="habit-info">
                        <a href="{{ url_for('habit-detail', habit_id=habit.id) }}">{{ habit.name }}</a>
                        <span class="streak" title="Дней подряд">🔥 {{ habit.streak }}</span>
                    </div>
                    <div class="habit-actions">
                        {% if not is_marked_today(habit.id) %}
                            <form action="{{ url_for('mark_habit_from_form', habit_id=habit.id) }}" method="post">
                                <button type="submit" class="btn btn-mark">Выполнил сегодня</button>
                            </form>
                        {% else %}
                            <span class="marked-today">✅ Отмечено!</span>
                        {% endif %}
                    </div>
                </div>
                {% endfor %}
            {% else %}
                <p>У вас пока нет привычек. Добавьте первую!</p>
            {% endif %}
        </div>

        <div class="add-habit-form">
            <h2>Добавить новую привычку</h2>
            <form action="{{ url_for('add_habit_from_form') }}" method="post">
                <input type="text" name="name" placeholder="Название привычки" required>
                <button type="submit" class="btn">Добавить</button>
            </form>
        </div>
        <div class="api-docs-link">
            <a href="/docs">Документация API (Swagger)</a>
        </div>
    </div>
</body>
</html>
```
Тебе не нужно верстать страницу с нуля, но важно, чтобы итоговый шаблон соответствовал требованиям ниже и корректно работал с твоим бэкендом.

Если ты изменяешь шаблон, **не ломай идентификаторы** (`id`, `class`), которые перечислены в требованиях — на них опирается JS-код.

#### 6.2. Файл `habit_tracker/templates/habit_detail.html`

Создай файл `habit_detail.html` со следующим содержимым: 

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Детали привычки: {{ habit.name }}</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <div class="container">
        <a href="{{ url_for('main-page') }}" class="back-link">&larr; К списку привычек</a>
        <h1>{{ habit.name }}</h1>
        <p class="streak">Текущая серия: 🔥 {{ habit.streak }}</p>

        <div class="edit-form">
            <h2>Редактировать привычку</h2>
            <form action="{{ url_for('edit_habit_from_form', habit_id=habit.id) }}" method="post">
                <input type="text" name="name" value="{{ habit.name }}" required>
                <button type="submit" class="btn">Сохранить</button>
            </form>
        </div>

        <div class="marks-history">
            <h2>История выполнений</h2>
            {% if habit.marks %}
                <ul>
                    {% for mark in habit.marks|sort(reverse=True) %}
                    <li>{{ mark.strftime('%d.%m.%Y') if mark is date else mark }}</li>
                    {% endfor %}
                </ul>
            {% else %}
                <p>Пока нет отметок.</p>
            {% endif %}
        </div>

        <div class="delete-action">
            <form action="{{ url_for('delete_habit_from_form', habit_id=habit.id) }}" method="post" onsubmit="return confirm('Вы уверены, что хотите удалить эту привычку?');">
                <button type="submit" class="btn btn-danger">Удалить привычку</button>
            </form>
        </div>
    </div>
</body>
</html>
```
Его нужно подключить и, если хочется, слегка адаптировать под твои модели/сервисы, сохранив ключевые элементы интерфейса.
Как и для главной страницы, важно сохранить указанные `id` элементов.

### 7. Файл `habit_tracker/static/js/script.js`

Интегрируй готовый JS-файл для взаимодействия с API

Создай пустой `script.js`, его можно будет использовать для интеграции JS-скриптов в работу с кодом.

### 8. Файл `habit_tracker/static/css/style.css`

Подключи готовые стили для веб-интерфейса

Создай файл стилей `style.css` со следующим содержимым: 

```css
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background-color: #f4f7f6;
    color: #333;
    margin: 0;
    padding: 20px;
}

.container {
    max-width: 700px;
    margin: 0 auto;
    background-color: #fff;
    padding: 20px 40px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

h1 {
    text-align: center;
    color: #2c3e50;
    margin-bottom: 30px;
}

h2 {
    color: #34495e;
    border-bottom: 2px solid #ecf0f1;
    padding-bottom: 10px;
    margin-top: 40px;
}

.habit-list {
    margin-top: 20px;
}

.habit-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 5px;
    margin-bottom: 10px;
    transition: background-color 0.2s;
}

.habit-item:hover {
    background-color: #fafafa;
}

.habit-info a {
    font-size: 1.2em;
    font-weight: 500;
    text-decoration: none;
    color: #2980b9;
}

.habit-info a:hover {
    text-decoration: underline;
}

.streak {
    margin-left: 15px;
    font-size: 1.1em;
    color: #e67e22;
    background-color: #fdf2e9;
    padding: 3px 8px;
    border-radius: 10px;
    font-weight: bold;
}

.btn {
    padding: 8px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1em;
    color: white;
    background-color: #3498db;
    transition: background-color 0.2s;
}

.btn:hover {
    background-color: #2980b9;
}

.btn-mark {
    background-color: #2ecc71;
}

.btn-mark:hover {
    background-color: #27ae60;
}

.btn-danger {
    background-color: #e74c3c;
}

.btn-danger:hover {
    background-color: #c0392b;
}

.marked-today {
    color: #27ae60;
    font-weight: bold;
}

.add-habit-form, .edit-form {
    margin-top: 30px;
}

form {
    display: flex;
    gap: 10px;
}

input[type="text"] {
    flex-grow: 1;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 1em;
}

.back-link {
    display: inline-block;
    margin-bottom: 20px;
    color: #3498db;
    text-decoration: none;
}

.marks-history ul {
    list-style-type: none;
    padding: 0;
}

.marks-history li {
    background-color: #ecf0f1;
    padding: 8px;
    border-radius: 3px;
    margin-bottom: 5px;
}

.delete-action {
    margin-top: 30px;
    border-top: 1px solid #eee;
    padding-top: 20px;
}

.api-docs-link {
    text-align: center;
    margin-top: 40px;
    font-size: 0.9em;
}
```

Ты можешь расширять стили под свой вкус, но не удаляй ключевые классы, на которые опирается разметка (`.habit-card`, `.mark-btn`, `.stats` и т.д.).

### 9. Обновить `requirements.txt`

Добавь новые зависимости для веб-интерфейса:
- `jinja2==3.1.2` — для работы с HTML-шаблонами
- `python-multipart==0.0.6` — для обработки форм (Form data)

**Важно:** Эти зависимости необходимы для работы веб-интерфейса. FastAPI использует `jinja2` для рендеринга шаблонов через `Jinja2Templates`, а `python-multipart` — для парсинга данных форм (`Form(...)`).

## API эндпоинты (полный список)

### JSON API (префикс `/api`)

| Метод | Путь | Описание | Статус |
|-------|------|----------|--------|
| POST | `/api/habits/` | Создать привычку | 201 |
| GET | `/api/habits/` | Список всех привычек | 200 |
| GET | `/api/habits/{id}/` | Получить одну привычку | 200 |
| PUT | `/api/habits/{id}/` | Обновить привычку | 200 |
| DELETE | `/api/habits/{id}/` | Удалить привычку | 204 |
| POST | `/api/habits/{id}/mark/` | Отметить выполнение | 200 |

### Web Interface

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/` | Главная страница |
| GET | `/habit/{id}/` | Детальная страница |


## Чек-лист перед сдачей

### Структура проекта
- [ ] Файл `habits.py` переименован в `habits_api.py`
- [ ] Создана папка `views/`
- [ ] Создан файл `views/web.py`
- [ ] Создана папка `templates/`
- [ ] Созданы файлы `index.html` и `habit_detail.html`
- [ ] Создана папка `static/css/` и `static/js/`
- [ ] Созданы файлы `style.css` и `script.js`

### API функциональность
- [ ] Все старые эндпоинты работают с префиксом `/api`
- [ ] `GET /api/habits/{id}/` возвращает одну привычку (200)
- [ ] `PUT /api/habits/{id}/` обновляет привычку (200)
- [ ] `DELETE /api/habits/{id}/` удаляет привычку (204)
- [ ] Все эндпоинты возвращают `streak` в ответе

### Web Interface
- [ ] Главная страница (`/`) отображается корректно
- [ ] Список привычек отображается на главной
- [ ] Кнопка "Выполнил сегодня" работает
- [ ] Отображается счётчик streak для каждой привычки
- [ ] Детальная страница (`/habit/{id}/`) работает
- [ ] Форма редактирования работает
- [ ] Кнопка удаления работает
- [ ] CSS стили применяются
- [ ] JavaScript работает

### Бизнес-логика
- [ ] Функция `calculate_streak()` корректно рассчитывает streak
- [ ] Streak обновляется при отметке привычки
- [ ] Streak учитывает пропущенные дни

### Качество кода
- [ ] PEP 8 соблюдён
- [ ] Type hints для всех функций
- [ ] Docstrings для всех функций и классов
- [ ] Бизнес-логика в `services.py`
- [ ] Нет дублирования кода

### Документация
- [ ] Swagger доступен по `/docs`
- [ ] Все эндпоинты в Swagger
- [ ] README обновлён с описанием веб-интерфейса