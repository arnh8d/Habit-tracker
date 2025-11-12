"""API роуты для управления привычками."""

from typing import List
from fastapi import APIRouter, status
from habit_tracker.core import services
from habit_tracker.core.models import (
    HabitCreate,
    HabitResponse,
    HabitMarkResponse,
    HabitListResponse,
)

router = APIRouter()



@router.post("/habits/", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit(habit: HabitCreate):
    """Создать новую привычку."""
    # 1. Вызвать services.create_habit() с habit.name
    created_habit = services.create_habit(habit.name)

    # 2. Вернуть HabitResponse с id и name созданной привычки
    return HabitResponse(id=created_habit.id, name=created_habit.name)



@router.post("/habits/{habit_id}/mark/", response_model=HabitMarkResponse)
def mark_habit(habit_id: int):
    """Отметить выполнение привычки за текущий день."""
    # 1. Вызвать services.mark_habit() с habit_id
    updated_habit = services.mark_habit(habit_id)

    # 2. Получить последнюю дату из habit.marks
    last_marked = updated_habit.marks[-1]

    # 3. Отформатировать дату в строку (YYYY-MM-DD)
    last_marked_str = last_marked.isoformat()

    # 4. Вернуть HabitMarkResponse
    return HabitMarkResponse(
        id=updated_habit.id,
        name=updated_habit.name,
        last_marked_at=last_marked_str,
    )



@router.get("/habits/", response_model=List[HabitListResponse])
def get_all_habits():
    """Получить список всех привычек."""
    # 1. Вызвать services.get_all_habits()
    all_habits = services.get_all_habits()

    # 2. Для каждой привычки создать HabitListResponse
    # 3. Преобразовать dates в список строк формата YYYY-MM-DD
    response = []
    for habit in all_habits:
        marks_str = [mark.isoformat() for mark in habit.marks]
        response.append(
            HabitListResponse(id=habit.id, name=habit.name, marks=marks_str)
        )

    # 4. Вернуть список
    return response
