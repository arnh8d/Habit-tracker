from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from habit_tracker.api.habits_api import router
from habit_tracker.views.web import router1
from pathlib import Path

app = FastAPI( title="Habit Tracker API")

current_file_path = Path(__file__).resolve()
static_path = current_file_path.parent / "static"

app.mount("/static", StaticFiles(directory=static_path), name="static")
app.include_router(router1, tags=["Web Interface"])
app.include_router(router, prefix="/api/habits", tags=["Habits API"])
