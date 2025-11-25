from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from habit_tracker.api import habits_api
from habit_tracker.views import web


app = FastAPI(title="Habit Tracker API")

app.mount("/static", StaticFiles(directory="habit_tracker/static"), name="static")

app.include_router(web.router, tags=["Web Interface"])
app.include_router(habits_api.router, prefix="/api/habits", tags=["Habits API"])
