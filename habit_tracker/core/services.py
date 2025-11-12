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

    # 1. Проверить, что name не пустое
    if not name or not name.strip():
        raise HTTPException(status_code=400, detail="Habit name cannot be empty.")

    name = name.strip()

    # 2. Проверить, что привычка с таким именем не существует
    for habit in habits_db.values():
        if habit.name == name:
            raise HTTPException(status_code=400, detail="Habit with this name already exists.")

    # 3. Создать объект Habit с текущим _next_id и name
    habit = Habit(id=_next_id, name=name)

    # 4. Сохранить в habits_db
    habits_db[_next_id] = habit

    # 5. Увеличить _next_id
    _next_id += 1

    # 6. Вернуть созданную привычку
    return habit



def mark_habit(habit_id: int) -> Habit:
    """Отметить выполнение привычки за текущий день."""
    # 1. Получить привычку из habits_db по habit_id
    habit = habits_db.get(habit_id)
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found.")

    # 2. Получить сегодняшнюю дату
    today = date.today()

    # 3. Проверить, что today не в habit.marks
    if today in habit.marks:
        raise HTTPException(status_code=400, detail="Habit already marked for today.")

    # 4. Добавить today в habit.marks
    habit.marks.append(today)

    # 5. Вернуть обновленную привычку
    return habit



def get_all_habits() -> List[Habit]:
    """Получить список всех привычек."""
    return list(habits_db.values())
