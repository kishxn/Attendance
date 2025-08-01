from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2

app = FastAPI()

# ✅ CORS fix
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Correct model matching HTML fields
class AttendanceEntry(BaseModel):
    site: str
    name: str
    date: str
    inout: str
    intime: str
    outtime: str
    reason: str
    approved_by: str

# ✅ Database connection
def get_conn():
    return psycopg2.connect(
        "postgresql://a_axbj_user:r57Ib3SXMZ75aOSrtv5cIW1fLveBOOeL@dpg-d264r3uuk2gs73bgv2kg-a.singapore-postgres.render.com/a_axbj"
    )

@app.get("/")
def home():
    return {"status": "FastAPI is running!"}

@app.post("/add/")
def add_entry(emp: AttendanceEntry):
    try:
        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Attendance (
            id SERIAL PRIMARY KEY,
            site TEXT,
            name TEXT,
            date DATE,
            inout TEXT,
            intime TIME,
            outtime TIME,
            reason TEXT,
            approved_by TEXT
        );
        """)

        cursor.execute("""
            INSERT INTO Attendance
            (site, name, date, inout, intime, outtime, reason, approved_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            emp.site,
            emp.name,
            emp.date,
            emp.inout,
            emp.intime,
            emp.outtime,
            emp.reason,
            emp.approved_by
        ))

        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "✅ Entry added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/view/")
def view_entries():
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT site, name, date, inout, intime, outtime, reason, approved_by FROM Attendance ORDER BY id DESC;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        attendance = []
        for row in rows:
            attendance.append({
                "site": row[0],
                "name": row[1],
                "date": row[2],
                "inout": row[3],
                "intime": str(row[4]) if row[4] else "",
                "outtime": str(row[5]) if row[5] else "",
                "reason": row[6],
                "approved_by": row[7]
            })
        return {"attendance": attendance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
