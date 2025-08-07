from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd

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

    df = pd.DataFrame([{
        "name": name,
        "mark": mark,
        "result": s.get_result(),
        "grade": Student.grade_from_mark(mark),
        "school": Student.get_school_name()
    }])

    html_table = df.to_html(index=False)

    # Optionally wrap inside full HTML document
    full_html = f"""
    <html>
    <head>
      <title>Student Result</title>
      <style>
        table {{
          width: 60%;
          border-collapse: collapse;
          margin: 20px auto;
        }}
        th, td {{
          border: 1px solid black;
          padding: 8px;
          text-align: center;
        }}
        th {{
          background-color: #f2f2f2;
        }}
      </style>
    </head>
    <body>
      <h2 style='text-align:center;'>Student Result</h2>
      {html_table}
    </body>
    </html>
    """

    return HTMLResponse(content=full_html)
