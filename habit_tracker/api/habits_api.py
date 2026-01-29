from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from habit_tracker.core import services, models
from habit_tracker.core.exceptions import *


router = APIRouter()


@router.post("/", response_model=models.HabitResponse, status_code=status.HTTP_201_CREATED)
def create_h(habit_data: models.HabitCreate):
    try:
        habit = services.create_habit(habit_data)
        return habit
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[models.HabitResponse])
def get_all_habits():
    habits = services.get_all_habits_with_details()
    return [
        models.HabitResponse(
            id=h["id"],
            name=h["name"],
            marks=h["marks"],
            streak=h["streak"],
        ) for h in habits
    ]


@router.get("/{habit_id}", response_model=models.HabitResponse)
def get_habit(habit_id: int):
    habit = services.get_habit_by_id_with_details(habit_id)
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found.")
    return models.HabitResponse(
        id=habit["id"],
        name=habit["name"],
        marks=habit["marks"],
        streak=habit["streak"],
    )


@router.put("/{habit_id}", response_model=models.HabitResponse)
def update_h(habit_id: int, habit_data: models.HabitUpdate):
    try:
        updated_habit = services.update_habit(habit_id, habit_data)
        if updated_habit is None:
            raise HTTPException(status_code=404, detail="Habit not found.")
        streak = services.calculate_streak(updated_habit.marks)
        return models.HabitResponse(
            id=updated_habit.id,
            name=updated_habit.name,
            marks=updated_habit.marks,
            streak=streak,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_h(habit_id: int):
    success = services.delete_habit(habit_id)
    if not success:
        raise HTTPException(status_code=404, detail="Habit not found.")
    return JSONResponse(content=None, status_code=204)


@router.post("/{habit_id}/mark", response_model=models.HabitMarkResponse)
def mark_h(habit_id: int):
    try:
        result = services.mark_habit(habit_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Habit not found.")
        last_marked_str = str(result["last_marked_at"].isoformat())
        return models.HabitMarkResponse(
            id=result["id"],
            name=result["name"],
            last_marked_at=last_marked_str,
            streak=result["streak"],
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
@router.get("/{habit_id}/stats", response_model=models.HabitStatsResponse)
def get_habit_stats(habit_id: int):
    habit = services.get_habit_by_id_with_details(habit_id)
    stats = services.calculate_streak(habit)
    return models.HabitStatsResponse(
        id=habit['id'],
        name=habit['name'],
        total_marks=stats["total_marks"],
        current_streak=stats["current_streak"],
        max_streak=stats["max_streak"],
        success_rate=stats["success_rate"],
        last_dates=stats["last_dates"]
    )