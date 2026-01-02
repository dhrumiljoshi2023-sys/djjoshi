# Troubleshooting Guide for Render Deployment

## Common Errors and Solutions

### 1. **Database Connection Errors**

**Error**: `Database connection error` or `could not connect to server`

**Solutions**:
- Verify all environment variables are set in Render Dashboard:
  - `DB_HOST` - Should be the hostname from your PostgreSQL service (not localhost)
  - `DB_NAME` - Database name from PostgreSQL service
  - `DB_USER` - Database user from PostgreSQL service
  - `DB_PASSWORD` - Database password from PostgreSQL service
  - `DB_PORT` - Usually 5432 (optional, defaults to 5432)

- Make sure your PostgreSQL database is running and accessible
- Check that your web service and database are in the same region
- Verify the database connection string in Render PostgreSQL dashboard

### 2. **Port Binding Errors**

**Error**: `Address already in use` or `Port not found`

**Solution**:
- Make sure your start command uses `$PORT`:
  ```
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```
- Render automatically sets the `$PORT` environment variable

### 3. **Module Not Found Errors**

**Error**: `ModuleNotFoundError: No module named 'fastapi'` or similar

**Solutions**:
- Verify `requirements.txt` includes all dependencies
- Check that build command is: `pip install -r requirements.txt`
- Ensure `runtime.txt` specifies Python version (e.g., `python-3.11.7`)

### 4. **Table Does Not Exist**

**Error**: `relation "employees" does not exist`

**Solution**:
- Run the SQL schema from `schema.sql` in your PostgreSQL database
- In Render, go to your PostgreSQL service → Connect → Use a database client
- Or use Render's built-in database shell to run:
  ```sql
  CREATE TABLE employees (
      id SERIAL PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      salary INTEGER NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  ```

### 5. **Build Failures**

**Error**: Build fails during `pip install`

**Solutions**:
- Check Python version compatibility in `runtime.txt`
- Ensure all package versions in `requirements.txt` are compatible
- Try updating package versions if build fails

### 6. **Application Crashes on Startup**

**Error**: Service crashes immediately after deployment

**Solutions**:
- Check logs in Render Dashboard → Logs tab
- Verify all environment variables are set correctly
- Ensure database is accessible from web service
- Check that start command is correct

### 7. **Environment Variables Not Set**

**Error**: `NoneType` errors or missing configuration

**Solution**:
- Go to Render Dashboard → Your Web Service → Environment
- Add all required environment variables:
  - `DB_HOST`
  - `DB_NAME`
  - `DB_USER`
  - `DB_PASSWORD`
  - `DB_PORT` (optional, defaults to 5432)

### 8. **SSL Connection Required**

**Error**: `SSL connection required` or `sslmode` errors

**Solution**:
- Render PostgreSQL requires SSL connections
- The code should handle this automatically, but if issues persist, you may need to add SSL parameters:
  ```python
  conn = psycopg2.connect(
      ...,
      sslmode='require'
  )
  ```

## How to Check Logs

1. Go to Render Dashboard
2. Click on your Web Service
3. Click on "Logs" tab
4. Review error messages and stack traces

## Testing Locally Before Deploying

1. Set up local `.env` file with database credentials
2. Run: `uvicorn main:app --reload`
3. Test all endpoints locally
4. Verify database connection works

## Quick Checklist

- [ ] All environment variables set in Render
- [ ] Database table created (run schema.sql)
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] `runtime.txt` file exists with Python version
- [ ] `requirements.txt` has all dependencies
- [ ] Database is running and accessible
- [ ] Web service and database in same region

