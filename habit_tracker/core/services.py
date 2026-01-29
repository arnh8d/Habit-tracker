import datetime
from habit_tracker.core.models import *
from habit_tracker.core.exceptions import *
from habit_tracker.db.session import SessionLocal, Habits

TODAY = datetime.date.today()

def calculate_max_streak(marks: list[date]):
    if not marks:
        return 0
    elif len(marks) == 1:
        return 1
    else:
        max_streak = 1
        current_streak = 1
        marks.sort(reverse=True)
        for i in range(1, len(marks)):
            prev_date = marks[i - 1]
            curr_date = marks[i]
            delta = (prev_date - curr_date).days
            if delta == 1:
                current_streak += 1
            else:
                current_streak = 1
            max_streak = max(max_streak, current_streak)
        return max_streak

def calculate_streak(marks: list[date]):
    if not marks or len(marks) == 0:
        return 0
    current_date = datetime.datetime.strptime(str(TODAY), "%Y-%m-%d")
    streak = 0
    while current_date in marks:

        streak += 1
        current_date -= datetime.timedelta(days=1)
    return streak

def get_all_habits_with_details():
    habits = SessionLocal()
    return [{
        "id": habit.id,
        "name": habit.name,
        "marks": habit.marks,
        "streak": calculate_streak(habit.marks)
    } for habit in habits.query(Habits).all()]

def get_habit_by_id_with_details(habit_id: int):
    habits = SessionLocal()
    habit = habits.query(Habits).filter(Habits.id == habit_id).first()
    if habit is None:
        return None
    streak = calculate_streak(habit.marks)
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
    if datetime.datetime.strptime(str(TODAY), "%Y-%m-%d") in habit.marks:
        raise HabitAlreadyMarkedTodayException()
    day = datetime.datetime.strptime(str(TODAY), "%Y-%m-%d")
    habit.marks.append(day)
    streak = calculate_streak(habit.marks)
    habit.streak = streak
    habits.commit()
    habits.close()
    return {
        'id':habit.id,
        'marks':habit.marks,
        'streak':streak
                }

def is_habit_marked_today(habit_id: int):
    habits = SessionLocal()
    habit = habits.query(Habits).filter(Habits.id == habit_id).first()
    if habit.marks is None:
        return False
    elif habit.marks == []:
        return False
    return str(TODAY) in habit.marks[-1][:10]
