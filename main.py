from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2

app = FastAPI()

# ✅ CORS fix to allow browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, use only specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Pydantic model
class Employee(BaseModel):
    name: str
    age: int
    department: str

# ✅ PostgreSQL DB connection (Render.com connection string)
def get_conn():
    return psycopg2.connect(
        "postgresql://a_axbj_user:r57Ib3SXMZ75aOSrtv5cIW1fLveBOOeL@dpg-d264r3uuk2gs73bgv2kg-a.singapore-postgres.render.com/a_axbj"
    )

# ✅ Home route
@app.get("/")
def read_root():
    return {"status": "FastAPI is running!"}

# ✅ Add employee
@app.post("/add/")
def add_employee(emp: Employee):
    try:
        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Attendance (
                id SERIAL PRIMARY KEY,
                site_name TEXT,
                name TEXT,
                entry_date DATE,
                entry_type TEXT,          -- 'In' or 'Out'
                actual_date DATE,         -- second date column
                entry_time TIME,
                reason TEXT,
                approved_by TEXT
);

        """)

        cursor.execute("""
    INSERT INTO Attendance
    (site_name, employee_name, entry_date, in_out, io_date, io_time, reason, approved_by)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
""", (
    emp.site_name,
    emp.employee_name,
    emp.entry_date,
    emp.in_out,
    emp.io_date,
    emp.io_time,
    emp.reason,
    emp.approved_by
))

        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Employee added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ View all employees
@app.get("/employees/")
def get_employees():
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT id, site_name, employee_name, entry_date FROM Attendance ORDER BY id;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        employees = [
            {"id": row[0], "name": row[1], "age": row[2], "department": row[3]}
            for row in rows
        ]

        return {"employees": employees}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
