"""
Database connection utilities
"""

import pyodbc
import psycopg2
from sqlalchemy import create_engine
import logging
from config.settings import MSSQL_CONFIG, POSTGRES_CONFIG

logger = logging.getLogger(__name__)


def get_mssql_connection():
    """Create SQL Server connection"""
    try:
        conn_str = (
            f"DRIVER={MSSQL_CONFIG['driver']};"
            f"SERVER={MSSQL_CONFIG['server']};"
            f"UID={MSSQL_CONFIG['username']};"
            f"PWD={MSSQL_CONFIG['password']};"
            f"TrustServerCertificate=yes"
        )
        connection = pyodbc.connect(conn_str)
        logger.info("SQL Server connection established")
        return connection
    except Exception as e:
        logger.error(f"Failed to connect to SQL Server: {e}")
        raise


def get_postgres_connection():
    """Create PostgreSQL connection"""
    try:
        connection = psycopg2.connect(
            host=POSTGRES_CONFIG['host'],
            user=POSTGRES_CONFIG['user'],
            password=POSTGRES_CONFIG['password'],
            database=POSTGRES_CONFIG['database'],
            port=POSTGRES_CONFIG['port']
        )
        logger.info("PostgreSQL connection established")
        return connection
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL: {e}")
        raise


def get_sqlalchemy_mssql_engine():
    """Create SQLAlchemy engine for SQL Server"""
    connection_string = (
        f"mssql+pyodbc://{MSSQL_CONFIG['username']}:"
        f"{MSSQL_CONFIG['password']}@"
        f"{MSSQL_CONFIG['server']}/{MSSQL_CONFIG['database']}"
        f"?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
    )
    engine = create_engine(connection_string)
    logger.info("SQLAlchemy MSSQL engine created")
    return engine
