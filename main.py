from fastapi import FastAPI
from typing import Optional
from fastapi.responses import JSONResponse

app = FastAPI()

class Student:
    school_name = "Bright Future School"

    def __init__(self, name, mark):
        self.name = name
        self.mark = mark

    def get_result(self):
        if self.mark >= 35:
            return f"{self.name} passed"
        else:
            return f"{self.name} failed"

    @classmethod
    def get_school_name(cls):
        return cls.school_name

    @staticmethod
    def grade_from_mark(mark):
        if mark >= 90:
            return "A+"
        elif mark >= 75:
            return "A"
        elif mark >= 60:
            return "B"
        elif mark >= 35:
            return "C"
        else:
            return "Fail"


@app.get("/")
def read_root():
    return {"message": "Welcome to Result Predictor API"}

@app.get("/predict")
def predict(name: str, mark: int):
    s = Student(name, mark)
    result_data= {
        "name": name,
        "mark": mark,
        "result": s.get_result(),
        "grade": Student.grade_from_mark(mark),
        "school": Student.get_school_name()
    }
    return JSONResponse(content=result_data)

