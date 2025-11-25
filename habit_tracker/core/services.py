from datetime import date, timedelta
from typing import Dict, List, Optional
from fastapi import HTTPException
from habit_tracker.core.models import Habit, HabitCreate, HabitUpdate


TODAY = date(2025, 7, 12)

habits_db: Dict[int, Habit] = {
    1: Habit(
        id=1,
        name="Бег",
        marks=[date(2025, 7, 10), date(2025, 7, 11)],
        streak=0
    ),
    2: Habit(
        id=2,
        name="Чтение",
        marks=[date(2025, 7, 11)],
        streak=0
    ),
    3: Habit(id=3, name="Медитация", marks=[], streak=0),
}
next_habit_id = 4

def calculate_streak(marks: List[date]) -> int:
    if not marks:
        return 0

    sorted_marks = sorted(set(marks), reverse=True)
    yesterday = TODAY - timedelta(days=1)

    if TODAY not in sorted_marks and yesterday not in sorted_marks:
        return 0

    streak = 0
    current_day = TODAY
    for mark in sorted_marks:
        if mark == current_day:
            streak += 1
            current_day -= timedelta(days=1)
        elif mark < current_day:
            break
    return streak

def get_all_habits_with_details() -> List[dict]:
    result = []
    for habit in habits_db.values():
        streak = calculate_streak(habit.marks)
        result.append({
            "id": habit.id,
            "name": habit.name,
            "marks": habit.marks,
            "streak": streak,
        })
    return sorted(result, key=lambda x: x["id"])

def get_habit_by_id_with_details(habit_id: int) -> Optional[dict]:

    habit = habits_db.get(habit_id)
    if habit is None:
        return None
    streak = calculate_streak(habit.marks)
    return {
        "id": habit.id,
        "name": habit.name,
        "marks": habit.marks,
        "streak": streak,
    }

def create_habit(habit_data: HabitCreate) -> Habit:

    global next_habit_id

    for habit in habits_db.values():
        if habit.name == habit_data.name:
            raise ValueError("Habit with this name already exists.")

    habit = Habit(
        id=next_habit_id,
        name=habit_data.name,
        marks=[],
        streak=0
    )
    habits_db[next_habit_id] = habit
    next_habit_id += 1
    return habit

def update_habit(habit_id: int, habit_data: HabitUpdate) -> Optional[Habit]:
    habit = habits_db.get(habit_id)
    if habit is None:
        return None


    for h in habits_db.values():
        if h.name == habit_data.name and h.id != habit_id:
            raise ValueError("Habit with this name already exists.")

    habit.name = habit_data.name
    return habit

def delete_habit(habit_id: int) -> bool:

    if habit_id in habits_db:
        del habits_db[habit_id]
        return True
    return False

def mark_habit(habit_id: int) -> Optional[dict]:

    habit = habits_db.get(habit_id)
    if habit is None:
        return None

    if TODAY in habit.marks:
        raise ValueError("Habit already marked for today.")

    habit.marks.append(TODAY)
    streak = calculate_streak(habit.marks)

    return {
        "id": habit.id,
        "name": habit.name,
        "last_marked_at": TODAY.isoformat(),
        "streak": streak,
    }

def is_habit_marked_today(habit_id: int) -> bool:
    habit = habits_db.get(habit_id)
    if habit is None:
        return False
    return TODAY in habit.marks
