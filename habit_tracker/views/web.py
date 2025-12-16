from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from habit_tracker.core import services

router1 = APIRouter()
templates = Jinja2Templates(directory="habit_tracker/templates")

@router1.get("/", name="main-page")
def main_page(request: Request):
    habits = services.get_all_habits_with_details()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "habits": habits,
            "is_marked_today": services.is_habit_marked_today,
        },
    )

@router1.get("/habit/{habit_id}/", name="habit-detail")
def habit_detail(request: Request, habit_id: int):
    habit = services.get_habit_by_id_with_details(habit_id)
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found.")
    return templates.TemplateResponse("habit_detail.html", {"request": request, "habit": habit})

@router1.post("/habit/add", name="add_habit_from_form")
def add_habit_from_form(name: str = Form(...)):
    try:
        habit_data = services.HabitCreate(name=name)
        services.create_habit(habit_data)
    except ValueError:
        pass
    return RedirectResponse(url=router1.url_path_for("main-page"), status_code=303)

@router1.post("/habit/{habit_id}/mark", name="mark_habit_from_form")
def mark_habit_from_form(habit_id: int):
    try:
        services.mark_habit(habit_id)
    except ValueError:
        pass
    return RedirectResponse(url=router1.url_path_for("main-page"), status_code=303)

@router1.post("/habit/{habit_id}/edit", name="edit_habit_from_form")
def edit_habit_from_form(habit_id: int, name: str = Form(...)):
    try:
        habit_data = services.HabitUpdate(name=name)
        services.update_habit(habit_id, habit_data)
    except ValueError:
        pass
    return RedirectResponse(
        url=router1.url_path_for("habit-detail", habit_id=habit_id),
        status_code=303,
    )

@router1.post("/habit/{habit_id}/delete", name="delete_habit_from_form")
def delete_habit_from_form(habit_id: int):
    services.delete_habit(habit_id)
    return RedirectResponse(url=router1.url_path_for("main-page"), status_code=303)
