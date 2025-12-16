from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from habit_tracker.core.models import *
from habit_tracker.core import services


router = APIRouter()


@router.post("/", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit(habit_data: HabitCreate):
    """Создание привычки."""
    try:
        habit = services.create_habit(habit_data)
        return HabitResponse(
            id=habit.id,
            name=habit.name,
            marks=habit.marks,
            streak=services.calculate_streak(habit.marks),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[HabitResponse])
def get_all_habits():
    """Список всех привычек."""
    habits = services.get_all_habits_with_details()
    return [
        HabitResponse(
            id=h["id"],
            name=h["name"],
            marks=h["marks"],
            streak=h["streak"],
        ) for h in habits
    ]


@router.get("/{id}/", response_model=HabitResponse)
def get_habit(id: int):
    """Получение одной привычки."""
    habit = services.get_habit_by_id_with_details(id)
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found.")
    return HabitResponse(
        id=habit["id"],
        name=habit["name"],
        marks=habit["marks"],
        streak=habit["streak"],
    )


@router.put("/{id}/", response_model=HabitResponse)
def update_habit(id: int, habit_data: HabitUpdate):
    """Обновление привычки."""
    try:
        updated_habit = services.update_habit(id, habit_data)
        if updated_habit is None:
            raise HTTPException(status_code=404, detail="Habit not found.")
        streak = services.calculate_streak(updated_habit.marks)
        return HabitResponse(
            id=updated_habit.id,
            name=updated_habit.name,
            marks=updated_habit.marks,
            streak=streak,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(id: int):
    """Удаление привычки."""
    success = services.delete_habit(id)
    if not success:
        raise HTTPException(status_code=404, detail="Habit not found.")
    return JSONResponse(content=None, status_code=204)


@router.post("/{id}/mark/", response_model=HabitMarkResponse)
def mark_habit(id: int):
    """Отметка выполнения привычки."""
    try:
        result = services.mark_habit(id)
        if result is None:
            raise HTTPException(status_code=404, detail="Habit not found.")


        last_marked_str = str(result["last_marked_at"].isoformat())
        return HabitMarkResponse(
            id=result["id"],
            name=result["name"],
            last_marked_at=last_marked_str,
            streak=result["streak"],
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
@router.get("/{habit_id}/stats/", response_model=HabitStatsResponse)
def get_habit_stats(habit_id: int):
    habit = get_habit(habit_id)
    stats = services.calculate_streak(habit)
    return HabitStatsResponse(
        id=habit.id,
        name=habit.name,
        total_marks=stats["total_marks"],
        current_streak=stats["current_streak"],
        max_streak=stats["max_streak"],
        success_rate=stats["success_rate"],
        last_dates=stats["last_dates"]
    )