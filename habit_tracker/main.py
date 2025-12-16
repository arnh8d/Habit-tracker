from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from habit_tracker.api.habits_api import *
from habit_tracker.views.web import router1
from pathlib import Path
from habit_tracker.core.exceptions import (
    HabitNotFoundException,
    HabitAlreadyMarkedTodayException,
    HabitNameConflictException,
    InvalidInputException)

app = FastAPI( title="Habit Tracker API")

current_file_path = Path(__file__).resolve()
static_path = current_file_path.parent / "static"

app.mount("/static", StaticFiles(directory=static_path), name="static")
app.include_router(router1, tags=["Web Interface"])
app.include_router(router, prefix="/api/habits", tags=["Habits API"])

@app.exception_handler(HabitNotFoundException)
async def habit_not_found_exception_handler(request: Request, exc: HabitNotFoundException):
    if request.url.path.startswith("/api"):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    return RedirectResponse(url="/?error=Habit+not+found", status_code=303)


@app.exception_handler(HabitAlreadyMarkedTodayException)
async def habit_already_marked_today_exception_handler(request: Request, exc: HabitAlreadyMarkedTodayException):
    if request.url.path.startswith("/api"):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    return RedirectResponse(url="/?error=Habit+already+marked+for+today", status_code=303)


@app.exception_handler(HabitNameConflictException)
async def habit_name_conflict_exception_handler(request: Request, exc: HabitNameConflictException):
    if request.url.path.startswith("/api"):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    return RedirectResponse(url="/?error=Habit+with+this+name+already+exists", status_code=303)


@app.exception_handler(InvalidInputException)
async def invalid_input_exception_handler(request: Request, exc: InvalidInputException):
    if request.url.path.startswith("/api"):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    return RedirectResponse(url="/?error=Invalid+input+data", status_code=303)