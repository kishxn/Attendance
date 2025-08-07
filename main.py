from fastapi import FastAPI
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

@app.get("/")
def root():
    return {"message": "Hello from Render!"}

@app.get("/predict")
def predict(name: str, mark: int):
    result = "Pass" if mark >= 35 else "Fail"
    return {"name": name, "mark": mark, "result": result}