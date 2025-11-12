"""Точка входа приложения Habit Tracker."""

from fastapi import FastAPI
from habit_tracker.api import habits

app = FastAPI(title="Habit Tracker API")

app.include_router(habits.router)
