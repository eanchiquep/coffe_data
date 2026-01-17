# Data Engineering Environment Setup

## Overview
This Docker setup provides a complete data engineering environment with:
- **SQL Server**: Relational database
- **Python 3.11**: Latest stable Python with data engineering tools
- **Apache Airflow 2.7.3**: Workflow orchestration
- **PostgreSQL**: Airflow metadata database
- **Redis**: Task queue for Airflow
- **Data Libraries**: pandas, numpy, sqlalchemy, polars, pyspark, dbt, and more

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- At least 4GB RAM available
- Port 8080, 1433, 5432, 6379 available

### Setup and Run

1. **Build the Docker image:**
   ```bash
   docker-compose build
   ```

2. **Start all services:**
   ```bash
   docker-compose up -d
   ```

3. **Access Airflow UI:**
   - Open browser: `http://localhost:8080`
   - Default username: `airflow`
   - Default password: `airflow`

4. **Connect to SQL Server:**
   - Host: `mssql` (from within containers) or `localhost:1433`
   - Username: `SA`
   - Password: `SqlServer@2026`
   - Database: `master`

5. **PostgreSQL (Airflow metadata):**
   - Host: `localhost:5432`
   - Username: `airflow`
   - Password: `Airflow@2026`
   - Database: `airflow`

### Directory Structure
```
coffe_data/
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── dags/                 # Airflow DAG files (create this)
├── logs/                 # Airflow logs (auto-created)
├── plugins/              # Custom Airflow plugins (create this)
└── data/                 # Data files for processing (create this)
```

## Creating DAG Directory

Create the required directories for Airflow:
```bash
mkdir -p dags logs plugins data
```

## Example Python Script

Create a test script to verify connectivity:

```python
# test_connections.py
import pandas as pd
import pyodbc
from airflow import DAG
from datetime import datetime

# SQL Server connection
conn_str = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=mssql;UID=SA;PWD=SqlServer@2026;TrustServerCertificate=yes'
try:
    cnxn = pyodbc.connect(conn_str)
    cursor = cnxn.cursor()
    cursor.execute('SELECT @@VERSION')
    print(cursor.fetchone())
    cnxn.close()
    print("✓ SQL Server connected successfully")
except Exception as e:
    print(f"✗ SQL Server connection failed: {e}")

# Pandas test
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
print("✓ Pandas working:", df.shape)

# PySpark test
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("test").getOrCreate()
print("✓ PySpark ready")
```

## Environment Variables

Edit the `MSSQL_PASSWORD` in `docker-compose.yml` to change SQL Server password. Common variables:

| Variable | Default | Purpose |
|----------|---------|---------|
| `SA_PASSWORD` | `SqlServer@2026` | SQL Server admin password |
| `POSTGRES_PASSWORD` | `Airflow@2026` | PostgreSQL Airflow password |
| `POSTGRES_PASSWORD` | `airflow_password` | PostgreSQL password for Airflow |
| `AIRFLOW__CORE__LOAD_EXAMPLES` | `False` | Disable example DAGs |

## Installed Python Libraries

### Data Processing
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `polars` - Fast DataFrame library
- `pyspark` - Distributed computing

### Database
- `sqlalchemy` - SQL toolkit and ORM
- `pyodbc` - SQL Server driver
- `psycopg2-binary` - PostgreSQL driver
- `pymongo` - MongoDB driver

### Analytics & ML
- `scikit-learn` - Machine learning
- `matplotlib` - Visualization
- `seaborn` - Statistical visualization

### Orchestration & Tools
- `apache-airflow` - Workflow orchestration
- `dbt-core` & `dbt-sqlserver` - Data build tool
- `jupyter` & `jupyterlab` - Interactive notebooks

## Common Commands

```bash
# View logs
docker-compose logs -f data-engineer

# Stop services
docker-compose down

# Remove volumes (careful! deletes data)
docker-compose down -v

# Execute command in container
docker-compose exec data-engineer python script.py

# Access Airflow CLI
docker-compose exec data-engineer airflow dags list
```

## Troubleshooting

**Port already in use:**
Modify port mappings in `docker-compose.yml`

**SQL Server connection fails:**
- Ensure SQL Server container is running: `docker-compose ps`
- Wait 30 seconds for SQL Server to initialize
- Verify password in connection string matches compose file

**Airflow not loading:**
- Check logs: `docker-compose logs data-engineer`
- Ensure PostgreSQL is healthy: `docker-compose logs postgres`

## Security Notes

⚠️ Change default passwords in production:
- Update `SA_PASSWORD` in docker-compose.yml
- Update `POSTGRES_PASSWORD` in docker-compose.yml
- Use `.env` file for sensitive data
