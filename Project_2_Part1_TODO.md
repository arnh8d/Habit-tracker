# Прооект 2. Часть 1: Базовый REST API для управления привычками

## Описание задачи

Создай REST API для управления привычками с базовым функционалом: добавление привычки, отметка выполнения и получение списка привычек.


## Цель

Освоить навыки реализации REST API на Python, работы с HTTP-методами, обработки JSON-данных, организации бизнес-логики и хранения данных (in-memory).

## Структура проекта

### ВАЖНО! Строго придерживайся этой структуры для прохождения автотестов!

```
project_root/
├── habit_tracker/             # Обязательное имя пакета
│   ├── __init__.py            # Пустой файл
│   │
│   ├── api/                   # Обязательная папка для роутов
│   │   ├── __init__.py        # Пустой файл
│   │   └── habits.py          # Обязательное имя файла с роутами
│   │
│   ├── core/                  # Обязательная папка для бизнес-логики
│   │   ├── __init__.py        # Пустой файл
│   │   ├── models.py          # Модели данных (Habit, Pydantic-модели)
│   │   └── services.py        # Бизнес-логика (функции работы с привычками)
│   │
│   └── main.py                # Точка входа приложения
│
├── .env.example               # Пример файла переменных окружения
├── requirements.txt           # Обязательный файл зависимостей
└── README.md                  # Документация проекта
```

## Требования к реализации

### 1. Файл `habit_tracker/main.py`

**Задача:** Создай точку входа приложения с инициализацией FastAPI

**Требования:**
- Создай экземпляр FastAPI с названием "Habit Tracker API"
- Имя переменной должно быть `app` (для автотестов!)
- Подключи роутер из модуля `habits`

**Пример структуры:**
```python
"""Точка входа приложения Habit Tracker."""

from fastapi import FastAPI
from habit_tracker.api import habits

# TODO: Создать экземпляр FastAPI
app = ...

# TODO: Подключить роутер
```

### 2. Файл `habit_tracker/core/models.py`

**Задача:** Создай модели данных для привычек

#### 2.1. Внутренняя модель привычки

**Требования:**
- Класс должен называться `Habit` (для автотестов!)
- Поля: `id` (int), `name` (str), `marks` (List[date])
- `marks` должен быть пустым списком при создании

**Пример структуры:**
```python
"""Модели данных для привычек."""

from datetime import date
from typing import List
from pydantic import BaseModel, validator


class Habit:
    """Внутренняя модель привычки для хранения в памяти."""
    
    def __init__(self, id: int, name: str):
        # TODO: Инициализировать поля
        pass
```

#### 2.2. Pydantic модели для API

**Требования:**
- `HabitCreate` - модель для создания (поле `name`)
- `HabitResponse` - ответ после создания (поля `id`, `name`)
- `HabitMarkResponse` - ответ после отметки (поля `id`, `name`, `last_marked_at`)
- `HabitListResponse` - для списка (поля `id`, `name`, `marks`)

**Подсказка:** Используй Pydantic validator для валидации `name` (не должно быть пустым)

**Пример структуры:**
```python
class HabitCreate(BaseModel):
    """Модель для создания привычки."""
    name: str
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        # TODO: Реализовать проверку на пустое имя
        pass

class HabitResponse(BaseModel):
    """Модель ответа после создания привычки."""
    # TODO: Добавить поля id и name
    pass

# TODO: Реализовать остальные модели (HabitMarkResponse, HabitListResponse)
```

### 3. Файл `habit_tracker/core/services.py`

**Задача:** Реализуй бизнес-логику работы с привычками

**Требования:**
- Используй in-memory хранилище `habits_db: Dict[int, Habit]`
- Реализуй функции: `create_habit()`, `mark_habit()`, `get_all_habits()`
- Используй HTTPException для обработки ошибок

**Обязательные имена (для автотестов):**
- Функция создания: `create_habit(name: str) -> Habit`
- Функция отметки: `mark_habit(habit_id: int) -> Habit`
- Функция получения списка: `get_all_habits() -> List[Habit]`
- Переменная хранилища: `habits_db`
- Счётчик ID: `_next_id`

**Пример структуры:**
```python
"""Бизнес-логика для работы с привычками."""

from datetime import date
from typing import Dict, List
from fastapi import HTTPException
from habit_tracker.core.models import Habit

# In-memory хранилище
habits_db: Dict[int, Habit] = {}
_next_id = 1


def create_habit(name: str) -> Habit:
    """Создать новую привычку."""
    global _next_id
    
    # TODO: 1. Проверить, что name не пустое
    #          Если пустое - raise HTTPException(status_code=400, detail="Habit name cannot be empty.")
    
    # TODO: 2. Проверить, что привычка с таким именем не существует
    #          Если существует - raise HTTPException(status_code=400, detail="Habit with this name already exists.")
    
    # TODO: 3. Создать объект Habit с текущим _next_id и name
    
    # TODO: 4. Сохранить в habits_db
    
    # TODO: 5. Увеличить _next_id
    
    # TODO: 6. Вернуть созданную привычку
    pass


def mark_habit(habit_id: int) -> Habit:
    """Отметить выполнение привычки за текущий день."""
    
    # TODO: 1. Получить привычку из habits_db по habit_id
    #          Если не найдена - raise HTTPException(status_code=404, detail="Habit not found.")
    
    # TODO: 2. Получить сегодняшнюю дату (date.today())
    
    # TODO: 3. Проверить, что today не в habit.marks
    #          Если уже есть - raise HTTPException(status_code=400, detail="Habit already marked for today.")
    
    # TODO: 4. Добавить today в habit.marks
    
    # TODO: 5. Вернуть обновленную привычку
    pass


def get_all_habits() -> List[Habit]:
    """Получить список всех привычек."""
    # TODO: Вернуть список всех привычек из habits_db
    pass
```

### 4. Файл `habit_tracker/api/habits.py`

**Задача:** Создай API эндпоинты для работы с привычками

**Требования:**
- Роутер должен быть в переменной `router` (для автотестов!)
- Реализуй 3 эндпоинта:
  - `POST /habits/` - создание привычки (возвращает 201)
  - `POST /habits/{habit_id}/mark/` - отметка выполнения (возвращает 200)
  - `GET /habits/` - получение списка (возвращает 200)
- Используй функции из `services`
- Используй response_model для типизации ответов

**Пример структуры:**
```python
"""API роуты для управления привычками."""

from typing import List
from fastapi import APIRouter, status
from habit_tracker.core import services
from habit_tracker.core.models import (
    HabitCreate, 
    HabitResponse, 
    HabitMarkResponse,
    HabitListResponse
)

router = APIRouter()


@router.post("/habits/", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit(habit: HabitCreate):
    """Создать новую привычку."""
    # TODO: 1. Вызвать services.create_habit() с habit.name
    # TODO: 2. Вернуть HabitResponse с id и name созданной привычки
    pass


@router.post("/habits/{habit_id}/mark/", response_model=HabitMarkResponse)
def mark_habit(habit_id: int):
    """Отметить выполнение привычки за текущий день."""
    # TODO: 1. Вызвать services.mark_habit() с habit_id
    # TODO: 2. Получить последнюю дату из habit.marks
    # TODO: 3. Отформатировать дату в строку (YYYY-MM-DD)
    # TODO: 4. Вернуть HabitMarkResponse
    pass


@router.get("/habits/", response_model=List[HabitListResponse])
def get_all_habits():
    """Получить список всех привычек."""
    # TODO: 1. Вызвать services.get_all_habits()
    # TODO: 2. Для каждой привычки создать HabitListResponse
    # TODO: 3. Преобразовать dates в список строк формата YYYY-MM-DD
    # TODO: 4. Вернуть список
    pass
```

### 5. Файл `requirements.txt`

**Задача:** Укажи необходимые зависимости проекта

**Требования:**
- FastAPI версии 0.104.1
- Uvicorn с поддержкой стандартных возможностей
- Pydantic для валидации
- Python-dotenv для работы с переменными окружения

### 6. Файл `.env.example`

**Задача:** Создай пример файла с переменными окружения

Добавь переменную `APP_ENV` со значением "development"

## API эндпоинты

### 1. POST /habits/ - Создать привычку

**Запрос:**
```http
POST /habits/ HTTP/1.1
Content-Type: application/json

{
  "name": "Бег"
}
```

**Ответы:**

**Успех (201 Created):**
```json
{
  "id": 1,
  "name": "Бег"
}
```

**Ошибка - пустое имя (400 Bad Request):**
```json
{
  "detail": "Habit name cannot be empty."
}
```

**Ошибка - дубликат (400 Bad Request):**
```json
{
  "detail": "Habit with this name already exists."
}
```

### 2. POST /habits/{habit_id}/mark/ - Отметить выполнение

**Запрос:**
```http
POST /habits/1/mark/ HTTP/1.1
```

**Ответы:**

**Успех (200 OK):**
```json
{
  "id": 1,
  "name": "Бег",
  "last_marked_at": "2025-07-07"
}
```

**Ошибка - не найдена (404 Not Found):**
```json
{
  "detail": "Habit not found."
}
```

**Ошибка - уже отмечена (400 Bad Request):**
```json
{
  "detail": "Habit already marked for today."
}
```

### 3. GET /habits/ - Получить список

**Запрос:**
```http
GET /habits/ HTTP/1.1
```

**Ответ (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Бег",
    "marks": ["2025-07-06", "2025-07-07"]
  },
  {
    "id": 2,
    "name": "Чтение",
    "marks": ["2025-07-07"]
  }
]
```

**Если привычек нет:**
```json
[]
```


## Запуск приложения

### 1. Создать виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

### 2. Установить зависимости

```bash
pip install -r requirements.txt
```

### 3. Запустить приложение

```bash
uvicorn habit_tracker.main:app --reload
```

## Чек-лист перед сдачей

### Структура проекта
- [ ] Создана папка `habit_tracker/`
- [ ] Создан файл `habit_tracker/__init__.py`
- [ ] Создана папка `habit_tracker/api/`
- [ ] Создан файл `habit_tracker/api/__init__.py`
- [ ] Создан файл `habit_tracker/api/habits.py`
- [ ] Создана папка `habit_tracker/core/`
- [ ] Создан файл `habit_tracker/core/__init__.py`
- [ ] Создан файл `habit_tracker/core/models.py`
- [ ] Создан файл `habit_tracker/core/services.py`
- [ ] Создан файл `habit_tracker/main.py`
- [ ] Создан файл `requirements.txt`
- [ ] Создан файл `README.md`

### Функциональность
- [ ] `POST /habits/` создает привычку и возвращает 201
- [ ] `POST /habits/` проверяет пустое имя (400)
- [ ] `POST /habits/` проверяет дубликат имени (400)
- [ ] `POST /habits/{id}/mark/` отмечает привычку (200)
- [ ] `POST /habits/{id}/mark/` возвращает 404 если не найдена
- [ ] `POST /habits/{id}/mark/` возвращает 400 если уже отмечена сегодня
- [ ] `GET /habits/` возвращает список всех привычек (200)
- [ ] `GET /habits/` возвращает пустой массив если привычек нет

### Качество кода
- [ ] Соблюдён PEP 8
- [ ] Все функции имеют type hints
- [ ] Все функции и классы имеют docstrings
- [ ] Бизнес-логика находится в `services.py`, а не в роутах
- [ ] Нет дублирования кода
- [ ] Нет циклических импортов

### Документация
- [ ] Swagger доступен по `/docs`
- [ ] Все эндпоинты корректно отображаются в Swagger
- [ ] README.md содержит инструкции по запуску
- [ ] README.md содержит примеры использования API

### Тестирование
- [ ] Приложение запускается без ошибок
- [ ] Можно создать привычку через Swagger
- [ ] Можно отметить привычку
- [ ] Можно получить список привычек
- [ ] Обработка ошибок работает корректно
