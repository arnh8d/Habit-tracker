from datetime import date
from typing import List, Optional
from pydantic import BaseModel, validator



class Habit:

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.marks: List[date] = []
        self.streak: int = 0  # Новое поле



class HabitCreate(BaseModel):
    name: str

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Habit name cannot be empty.")
        return v.strip()



class HabitUpdate(BaseModel):
    name: str

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Habit name cannot be empty.")
        return v.strip()



class HabitBase(BaseModel):
    id: int
    name: str



class HabitResponse(HabitBase):
    marks: List[date]
    streak: int



class HabitMarkResponse(HabitBase):
    last_marked_at: str
    streak: int



class HabitListResponse(HabitResponse):
    pass



class HabitDetailResponse(HabitResponse):
    pass
