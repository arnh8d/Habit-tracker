from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from habit_tracker.core import services, models, exceptions

webrouter = APIRouter()


templates = Jinja2Templates(directory='habit_tracker/templates')

@webrouter.get("/", name="main-page")
def main_page(request: Request):
    habits = services.get_all_habits_with_details()
    is_marked_map = {
        habit['id']: services.is_habit_marked_today(habit['id'])
        for habit in habits
    }
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "habits": habits,
            "is_marked_today": is_marked_map,
        },
    )

@webrouter.get("/habit/{habit_id}", name="habit-detail")
def habit_detail(request: Request, habit_id: int):
    habit = services.get_habit_by_id_with_details(habit_id)
    if habit is None:
        raise exceptions.HTTPException(status_code=404, detail="Habit not found.")
    return templates.TemplateResponse("habit_detail.html", {"request": request, "habit": habit})

@webrouter.post("/habit/add", name="add_habit_from_form")
def add_habit_from_form(request:Request,name: str = Form(...)):
    try:
        habit_data = models.HabitCreate(name=name)
        services.create_habit(habit_data)
    except ValueError:
        pass
    return main_page(request)

@webrouter.post("/habit/{habit_id}/mark")
def mark_habit_from_form(request:Request,habit_id: int):
    try:
        services.mark_habit(habit_id)
    except ValueError:
        pass
    return main_page(request)

@webrouter.post("/habit/{habit_id}/edit")
def edit_habit_from_form(request:Request,habit_id: int, name: str = Form(...)):
    try:
        habit_data = services.HabitUpdate(name=name)
        services.update_habit(habit_id, habit_data)
        habit = services.get_habit_by_id_with_details(habit_id)
    except ValueError:
        pass
    return templates.TemplateResponse('habit_detail.html', {"request": request, "habit": habit})

@webrouter.post("/habit/{habit_id}/delete")
def delete_habit_from_form(request:Request,habit_id: int):
    try:
        services.delete_habit(habit_id)
    except ValueError:
        pass
    return main_page(request)

@webrouter.get("/stats", name="stats-page", response_class=HTMLResponse)
def get_stats_page(request: Request):
    habits = services.get_all_habits_with_details()
    stats_data = []
    for habit in habits:
        stats = services.get_habit_stats(habit['id'])
        stats_data.append({
            "id": habit['id'],
            "name": habit['name'],
            "current_streak": stats.current_streak,
            "max_streak": stats.max_streak,
            "last_dates": stats.last_dates
        })
    return templates.TemplateResponse(
        "stats.html",
        {"request": request, "stats": stats_data}
    )
