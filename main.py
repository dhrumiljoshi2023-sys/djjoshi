from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import OperationalError
import os
from contextlib import contextmanager

app = FastAPI()

# ---------- MODEL ----------
class Emp(BaseModel):
    name: str
    salary: int


# ---------- DB CONNECTION ----------
@contextmanager
def get_conn():
    """Context manager for database connections with proper error handling"""
    conn = None
    try:
        # Render PostgreSQL requires SSL, but psycopg2 handles it automatically
        # If you get SSL errors, you may need to add: sslmode='require'
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            database=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            port=os.environ.get("DB_PORT", "5432"),
            cursor_factory=RealDictCursor,
            connect_timeout=10
        )
        yield conn
    except OperationalError as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Database connection error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Database error: {str(e)}"
        )
    finally:
        if conn:
            conn.close()


# ---------- HOME ----------
@app.get("/")
def home():
    return {"message": "FastAPI + PostgreSQL on Render is LIVE 🚀"}


# ---------- HEALTH CHECK ----------
@app.get("/health")
def health_check():
    """Health check endpoint for Render"""
    try:
        # Test database connection
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT 1")
            cur.fetchone()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}


# ---------- GET ALL ----------
@app.get("/employees")
def get_all():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM employees ORDER BY id")
        data = cur.fetchall()
        return data


# ---------- GET BY ID ----------
@app.get("/employees/{emp_id}")
def get_by_id(emp_id: int):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM employees WHERE id=%s", (emp_id,))
        data = cur.fetchone()
        
        if not data:
            raise HTTPException(status_code=404, detail="Employee not found")
        return data


# ---------- INSERT ----------
@app.post("/employees")
def insert_employee(emp: Emp):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO employees (name, salary) VALUES (%s, %s) RETURNING id",
            (emp.name, emp.salary)
        )
        new_id = cur.fetchone()["id"]
        conn.commit()
        return {"message": "Employee added", "id": new_id}


# ---------- UPDATE ----------
@app.put("/employees/{emp_id}")
def update_employee(emp_id: int, emp: Emp):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE employees SET name=%s, salary=%s WHERE id=%s",
            (emp.name, emp.salary, emp_id)
        )
        conn.commit()
        affected = cur.rowcount
        
        if affected == 0:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        return {"message": "Employee updated"}


# ---------- DELETE ----------
@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM employees WHERE id=%s", (emp_id,))
        conn.commit()
        affected = cur.rowcount
        
        if affected == 0:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        return {"message": "Employee deleted"}

