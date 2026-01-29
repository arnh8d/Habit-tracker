from datetime import date
from typing import List
from pydantic import BaseModel

class HabitStatsResponse(BaseModel):
    id: int
    name: str
    total_marks: int
    current_streak: int
    max_streak: int
    success_rate: float
    last_dates: list[date]

class Habit(BaseModel):
    id: int
    name: str
    marks: List[date] = []
    streak: int = 0


class HabitCreate(BaseModel):
    name: str


class HabitUpdate(BaseModel):
    name: str


class HabitBase(BaseModel):
    id: int
    name: str

class HabitResponse(HabitBase):
    marks: List[date]
    streak: int

class HabitMarkResponse(HabitBase):
    last_marked_at: str
    streak: int
