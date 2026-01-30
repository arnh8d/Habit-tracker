from datetime import date
from typing import List
from pydantic import BaseModel

class HabitStatsResponse(BaseModel):
    id: int
    name: str
    current_streak: int
    max_streak: int
    last_dates: str





class HabitCreate(BaseModel):
    name: str


class HabitUpdate(BaseModel):
    name: str


class HabitBase(BaseModel):
    id: int
    name: str

