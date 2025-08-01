from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2

app = FastAPI()

# CORS enabled for all origins (browser access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for Attendance
class AttendanceEntry(BaseModel):
    site: str
    name: str
    date: str  # Format: YYYY-MM-DD
    inout: str
    intime: str = None
    outtime: str = None
    reason: str
    approved_by: str

# DB connection function
def get_conn():
    return psycopg2.connect(
        "postgresql://a_axbj_user:r57Ib3SXMZ75aOSrtv5cIW1fLveBOOeL@dpg-d264r3uuk2gs73bgv2kg-a.singapore-postgres.render.com/a_axbj"
    )

# Root endpoint
@app.get("/")
def root():
    return {"message": "Attendance API working!"}

# Add Entry
@app.post("/add/")
def add_entry(entry: AttendanceEntry):
    try:
        conn = get_conn()
        cur = conn.cursor()

        # Table creation if not exists
        cur.execute("""
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

        # Insert data
        cur.execute("""
            INSERT INTO Attendance
            (site, name, date, inout, intime, outtime, reason, approved_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            entry.site, entry.name, entry.date, entry.inout,
            entry.intime, entry.outtime, entry.reason, entry.approved_by
        ))

        conn.commit()
        cur.close()
        conn.close()
        return {"message": "✅ Entry added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# View all
@app.get("/view/")
def view_entries():
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("SELECT site, name, date, inout, intime, outtime, reason, approved_by FROM Attendance ORDER BY id DESC;")
        rows = cur.fetchall()

        entries = []
        for row in rows:
            entries.append({
                "site": row[0],
                "name": row[1],
                "date": row[2],
                "inout": row[3],
                "intime": str(row[4]) if row[4] else "",
                "outtime": str(row[5]) if row[5] else "",
                "reason": row[6],
                "approved_by": row[7]
            })

        cur.close()
        conn.close()
        return {"attendance": entries}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
