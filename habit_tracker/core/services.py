import datetime
from habit_tracker.core.models import *
from habit_tracker.core.exceptions import *
from habit_tracker.db.session import SessionLocal, Habits

TODAY = datetime.date.today()

def get_habit_stats(habit_id: int):
    habit = get_habit_by_id_with_details(habit_id)
    return HabitStatsResponse(
        id=habit['id'],
        name=habit['name'],
        current_streak=calculate_streak(habit['marks']),
        max_streak=calculate_max_streak(habit['marks']),
        last_dates=habit['marks'][:10] if len(habit['marks'])>10 else habit['marks']
    )

def calculate_max_streak(marks: list[str]):
    if not marks:
        return 0
    elif len(marks) == 1:
        return 1
    else:
        max_streak = 1
        current_streak = 1
        marks.sort(reverse=True)
        for i in range(1, len(marks)):
            prev_date = datetime.datetime.strptime(marks[i-1], '%Y-%m-%d').date()
            curr_date = datetime.datetime.strptime(marks[i], '%Y-%m-%d').date()
            delta = (prev_date - curr_date).days
            if delta == 1:
                current_streak += 1
            else:
                current_streak = 1
            max_streak = max(max_streak, current_streak)
        return max_streak

def calculate_streak(marks: list[str]):
    if not marks or len(marks) == 0:
        return 0
    if len(marks) == 1:
        return 1
    current_date = TODAY
    streak = 0
    while str(current_date) in marks:
        streak += 1
        current_date -= datetime.timedelta(days=1)
    return streak

def get_all_habits_with_details():
    habits = SessionLocal()
    try:
        return [{
            "id": habit.id,
            "name": habit.name,
            "marks": habit.marks,
            "streak": habit.streak
        } for habit in habits.query(Habits).all()]
    finally:
        habits.close()

def get_habit_by_id_with_details(habit_id: int):
    habits = SessionLocal()
    habit = habits.query(Habits).filter(Habits.id == habit_id).first()
    if habit is None:
        raise HabitNotFoundException()
    habits.close()
    return {
        "id": habit.id,
        "name": habit.name,
        "marks": habit.marks,
        "streak": habit.streak
    }

def create_habit(habit_data: HabitCreate):
    habits = SessionLocal()
    try:
        if habits.query(Habits).filter(Habits.name == habit_data.name).first():
                raise HabitNameConflictException()
        habit = Habits(name=habit_data.name)
        habits.add(habit)
        habits.commit()
        return {
            "id": habit.id,
            "name": habit.name,
            "marks": habit.marks,
            "streak": habit.streak
        }
    except:
        habits.close()
        raise InvalidInputException()
    finally:
        habits.close()

def update_habit(habit_id: int, habit_data: HabitUpdate):
    habits = SessionLocal()
    habit = habits.query(Habits).filter(Habits.id == habit_id).first()
    if habit is None:
        habits.close()
        raise HabitNotFoundException()
    if habit.name == habit_data.name:
        habits.close()
        raise HabitNameConflictException()
    else:
        habit.name = habit_data.name
        habits.commit()
        habits.close()
        return True

def delete_habit(habit_id: int):
    habits = SessionLocal()
    habits.query(Habits).filter(Habits.id == habit_id).delete()
    habits.commit()
    habits.close()
    return True

def mark_habit(habit_id: int):
    habits = SessionLocal()
    habit = habits.query(Habits).filter(Habits.id == habit_id).first()
    today_str = datetime.date.today().strftime('%Y-%m-%d')
    marks_list = habit.marks
    if not isinstance(marks_list, list):
            marks_list = []
    if today_str in marks_list:
            raise HabitAlreadyMarkedTodayException()
    marks_list.append(today_str)
    streak = calculate_streak(marks_list)
    habit.marks = marks_list
    habit.streak = streak
    habits.add(habit)
    habits.flush()
    habits.commit()
    habits.close()
    return True

def is_habit_marked_today(habit_id: int):
    habit = get_habit_by_id_with_details(habit_id)
    if habit is None:
        raise HabitNotFoundException()
    elif len(habit['marks']) == 0 or habit['marks'] is None:
        return False
    else:
       return str(TODAY) in habit['marks']