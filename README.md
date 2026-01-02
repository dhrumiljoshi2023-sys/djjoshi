# FastAPI + PostgreSQL on Render

A RESTful API built with FastAPI and PostgreSQL, ready to deploy on Render.

## Features

- ✅ CRUD operations for employees
- ✅ PostgreSQL database integration
- ✅ FastAPI with automatic API documentation
- ✅ Environment variable configuration
- ✅ Ready for Render deployment

## API Endpoints

- `GET /` - Home endpoint
- `GET /employees` - Get all employees
- `GET /employees/{emp_id}` - Get employee by ID
- `POST /employees` - Create new employee
- `PUT /employees/{emp_id}` - Update employee
- `DELETE /employees/{emp_id}` - Delete employee

## Database Schema

Create the following table in your PostgreSQL database:

```sql
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    salary INTEGER NOT NULL
);
```

## Local Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <your-project-folder>
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Fill in your database credentials:
     ```
     DB_HOST=localhost
     DB_NAME=your_database
     DB_USER=your_user
     DB_PASSWORD=your_password
     ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

6. **Access the API**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Deploy to Render

### Step 1: Create PostgreSQL Database

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "PostgreSQL"
3. Fill in the database details and create it
4. Note down the connection details (host, database, user, password)

### Step 2: Create Web Service

1. In Render Dashboard, click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure the service:
   - **Name**: Your service name
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free or Paid (your choice)

### Step 3: Set Environment Variables

In your Render Web Service settings, add these environment variables:

- `DB_HOST` - Your PostgreSQL host (from Step 1)
- `DB_NAME` - Your PostgreSQL database name
- `DB_USER` - Your PostgreSQL user
- `DB_PASSWORD` - Your PostgreSQL password

### Step 4: Deploy

1. Click "Create Web Service"
2. Render will automatically build and deploy your application
3. Once deployed, you'll get a URL like: `https://your-app.onrender.com`

## API Usage Examples

### Create Employee
```bash
curl -X POST "https://your-app.onrender.com/employees" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "salary": 50000}'
```

### Get All Employees
```bash
curl "https://your-app.onrender.com/employees"
```

### Get Employee by ID
```bash
curl "https://your-app.onrender.com/employees/1"
```

### Update Employee
```bash
curl -X PUT "https://your-app.onrender.com/employees/1" \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Doe", "salary": 60000}'
```

### Delete Employee
```bash
curl -X DELETE "https://your-app.onrender.com/employees/1"
```

## Project Structure

```
.
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore file
├── README.md           # This file
└── render.yaml         # Render deployment config (optional)
```

## License

MIT

