from fastapi import HTTPException


class HabitNotFoundException(HTTPException):
    def __init__(self, detail: str = "Habit not found."):
        super().__init__(status_code=404, detail=detail)



class HabitAlreadyMarkedTodayException(HTTPException):
    def __init__(self, detail: str = "Habit already marked for today."):
        super().__init__(status_code=409, detail=detail)



class HabitNameConflictException(HTTPException):
    def __init__(self, detail: str = "Habit with this name already exists."):
        super().__init__(status_code=400, detail=detail)



class InvalidInputException(HTTPException):
    def __init__(self, detail: str = "Invalid input data."):
        super().__init__(status_code=400, detail=detail)
