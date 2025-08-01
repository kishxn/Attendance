from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2

app = FastAPI()

# CORS allow for browser usage
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model (should match the table)
class AttendanceEntry(BaseModel):
    site_name: str
    employee_name: str
    entry_date: str  # YYYY-MM-DD
    in_out: str
    io_date: str     # YYYY-MM-DD
    io_time: str     # HH:MM
    reason: str
    approved_by: str

# DB connection (update credentials if needed)
def get_conn():
    return psycopg2.connect(
        "postgresql://a_axbj_user:r57Ib3SXMZ75aOSrtv5cIW1fLveBOOeL@dpg-d264r3uuk2gs73bgv2kg-a.singapore-postgres.render.com/a_axbj"
    )

@app.post("/add/")
def add_entry(entry: AttendanceEntry):
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS Attendance (
                id SERIAL PRIMARY KEY,
                site_name TEXT NOT NULL,
                employee_name TEXT NOT NULL,
                entry_date DATE NOT NULL,
                in_out TEXT NOT NULL,
                io_date DATE NOT NULL,
                io_time TIME NOT NULL,
                reason TEXT,
                approved_by TEXT
            );
        """)

        cur.execute("""
            INSERT INTO Attendance
            (site_name, employee_name, entry_date, in_out, io_date, io_time, reason, approved_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            entry.site_name,
            entry.employee_name,
            entry.entry_date,
            entry.in_out,
            entry.io_date,
            entry.io_time,
            entry.reason,
            entry.approved_by
        ))

        conn.commit()
        cur.close()
        conn.close()
        return {"message": "✅ Entry added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/view/")
def view_entries():
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("SELECT site_name, employee_name, entry_date, in_out, io_date, io_time, reason, approved_by FROM Attendance ORDER BY id DESC;")
        rows = cur.fetchall()

        entries = []
        for row in rows:
            entries.append({
                "site_name": row[0],
                "employee_name": row[1],
                "entry_date": row[2],
                "in_out": row[3],
                "io_date": row[4],
                "io_time": str(row[5]),
                "reason": row[6],
                "approved_by": row[7]
            })

        cur.close()
        conn.close()
        return {"attendance": entries}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
