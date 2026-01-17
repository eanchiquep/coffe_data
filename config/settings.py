"""
Configuration settings for the data engineering project
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_PATH = PROJECT_ROOT / "data"
LOGS_PATH = PROJECT_ROOT / "logs"

# Database connections
MSSQL_CONFIG = {
    "server": os.getenv("SQL_SERVER_HOST", "localhost"),
    "username": os.getenv("SQL_SERVER_USER", "SA"),
    "password": os.getenv("SQL_SERVER_PASSWORD", "SqlServer@2026"),
    "database": os.getenv("SQL_SERVER_DATABASE", "master"),
    "driver": "ODBC Driver 18 for SQL Server"
}

POSTGRES_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "user": os.getenv("POSTGRES_USER", "airflow"),
    "password": os.getenv("POSTGRES_PASSWORD", "Airflow@2026"),
    "database": os.getenv("POSTGRES_DB", "airflow"),
    "port": os.getenv("POSTGRES_PORT", 5432)
}

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
