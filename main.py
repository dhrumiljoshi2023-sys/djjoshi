from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = FastAPI()

# ---------- MODEL ----------
class Emp(BaseModel):
    name: str
    salary: int


# ---------- DB CONNECTION ----------
def get_conn():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        cursor_factory=RealDictCursor
    )


# ---------- HOME ----------
@app.get("/")
def home():
    return {"message": "FastAPI + PostgreSQL on Render is LIVE 🚀"}


# ---------- GET ALL ----------
@app.get("/employees")
def get_all():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees ORDER BY id")
    data = cur.fetchall()
    conn.close()
    return data


# ---------- GET BY ID ----------
@app.get("/employees/{emp_id}")
def get_by_id(emp_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees WHERE id=%s", (emp_id,))
    data = cur.fetchone()
    conn.close()

    if not data:
        raise HTTPException(status_code=404, detail="Employee not found")
    return data


# ---------- INSERT ----------
@app.post("/employees")
def insert_employee(emp: Emp):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO employees (name, salary) VALUES (%s, %s) RETURNING id",
        (emp.name, emp.salary)
    )

    new_id = cur.fetchone()["id"]
    conn.commit()
    conn.close()

    return {"message": "Employee added", "id": new_id}


# ---------- UPDATE ----------
@app.put("/employees/{emp_id}")
def update_employee(emp_id: int, emp: Emp):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "UPDATE employees SET name=%s, salary=%s WHERE id=%s",
        (emp.name, emp.salary, emp_id)
    )

    conn.commit()
    affected = cur.rowcount
    conn.close()

    if affected == 0:
        raise HTTPException(status_code=404, detail="Employee not found")

    return {"message": "Employee updated"}


# ---------- DELETE ----------
@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DELETE FROM employees WHERE id=%s", (emp_id,))
    conn.commit()
    affected = cur.rowcount
    conn.close()

    if affected == 0:
        raise HTTPException(status_code=404, detail="Employee not found")

    return {"message": "Employee deleted"}

