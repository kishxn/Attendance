from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

class Student:
    school_name = "Bright Future School"

    def __init__(self, name, mark):
        self.name = name
        self.mark = mark

    def get_result(self):
        return f"{self.name} passed" if self.mark >= 35 else f"{self.name} failed"

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

@app.get("/predict", response_class=HTMLResponse)
def predict(name: str, mark: int):
    s = Student(name, mark)
    result = s.get_result()
    grade = Student.grade_from_mark(mark)
    school = Student.get_school_name()
    return f"{result} with grade {grade} from {school}"