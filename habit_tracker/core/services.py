import datetime
from habit_tracker.core.models import *
from habit_tracker.core.exceptions import *
from habit_tracker.db.session import SessionLocal, Habits

TODAY = datetime.date.today()

def calculate_max_streak(marks: list[date]):
    if not marks:
        return 0
    if len(marks) == 1:
        return 1
    max_streak = 1
    current_streak = 1
    for i in range(1, len(marks)):
        prev_date = marks[i - 1]
        curr_date = marks[i]
        delta = (curr_date - prev_date)
        if delta == 1:
            current_streak += 1
        else:
            current_streak = 1
        max_streak = max(max_streak, current_streak)
    return max_streak

def calculate_streak(marks: list[date]):
    if not marks:
        return 0
    current_date = TODAY
    streak = 0
    while current_date in marks:
        streak += 1
        current_date -= 1
    return streak

def get_all_habits_with_details():
    habits = SessionLocal()
    return habits.query(Habits).all()

def get_habit_by_id_with_details(habit_id: int):
    habits = SessionLocal()
    habit = habits.query(Habits).filter(Habit.id == habit_id).first()
    if habit is None:
        return None
    streak = calculate_streak(habit.streak)
    habits.close()
    return {
        "id": habit.id,
        "name": habit.name,
        "marks": habit.marks,
        "streak": streak
    }

def create_habit(habit_data: HabitCreate):
    habits = SessionLocal()
    if habits.query(Habits).filter(Habits.name == habit_data.name).first():
            raise HabitNameConflictException()
    habit = Habits(name=habit_data.name, marks=habit_data.marks)
    habits.add(habit)
    habits.commit()
    habits.close()
    return habit

def update_habit(habit_id: int, habit_data: HabitUpdate):
    habits = SessionLocal()
    habit = habits.query(Habits).filter(Habits.id == habit_id).first()
    if habit is None:
        return None
    if habit.name == habit_data.name:
        habits.close()
        raise HabitNameConflictException()
    else:
        habit.name = habit_data.name
        habits.close()
        return habit

def delete_habit(habit_id: int):
    habits = SessionLocal()
    if habit_id in habits:
        del habits[habit_id]
        return True
    habits.close()
    return False

def mark_habit(habit_id: int):
    habits = SessionLocal()
    habit = habits.query(Habits).filter(Habits.id == habit_id).first()
    if habit is None:
        return None
    if TODAY in habit.marks:
        raise HabitAlreadyMarkedTodayException()
    habit.marks.append(TODAY)
    streak = calculate_streak(habit.marks)
    habit.streak = streak
    habits.close()
    return habit

def is_habit_marked_today(habit_id: int):
    habits = SessionLocal()
    habit = habits.query(Habits).filter(Habits.id == habit_id).first()
    if habit is None:
        return False
    return TODAY in habit.marks
