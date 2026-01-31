from pydantic import BaseModel

class HabitStatsResponse(BaseModel):
    id: int
    name: str
    current_streak: int
    max_streak: int
    last_dates: list

class HabitCreate(BaseModel):
    name: str

class HabitUpdate(BaseModel):
    name: str

class HabitBase(BaseModel):
    id: int
    name: str