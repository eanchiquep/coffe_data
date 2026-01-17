# Multi-stage Dockerfile for Data Engineering with SQL Server, Python, and Apache Airflow

FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    AIRFLOW_HOME=/home/airflow \
    AIRFLOW__CORE__DAGS_FOLDER=/home/airflow/dags \
    AIRFLOW__CORE__LOAD_EXAMPLES=False \
    AIRFLOW__CORE__UNIT_TEST_MODE=True

# Install system dependencies including SQL Server ODBC driver
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    wget \
    gnupg \
    unixodbc \
    unixodbc-dev \
    apt-transport-https \
    git \
    ca-certificates

RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create airflow user
RUN useradd -m -d /home/airflow airflow

# Set working directory
WORKDIR /home/airflow

# Install Python data engineering libraries
RUN pip install --upgrade pip setuptools wheel && \
    pip install \
    apache-airflow==2.7.3 \
    apache-airflow-providers-apache-spark==4.5.0 \
    apache-airflow-providers-microsoft-mssql==3.5.0 \
    pandas==2.1.3 \
    numpy==1.24.3 \
    sqlalchemy==1.4.46 \
    pyodbc==4.0.39 \
    psycopg2-binary==2.9.9 \
    pymongo==4.6.0 \
    pyspark==3.5.0 \
    polars==0.19.19 \
    dbt-core==1.7.2 \
    dbt-sqlserver==1.7.4 \
    jupyter==1.0.0 \
    jupyterlab==4.0.9 \
    scikit-learn==1.3.2 \
    matplotlib==3.8.2 \
    seaborn==0.13.0 \
    requests==2.31.0 \
    python-dotenv==1.0.0 \
    pydantic==2.5.0 \
    flask-session==0.5.0

# Initialize Airflow database
RUN airflow db migrate

# Create necessary directories
RUN mkdir -p /home/airflow/dags \
    && mkdir -p /home/airflow/logs \
    && mkdir -p /home/airflow/plugins \
    && chown -R airflow:airflow /home/airflow

# Switch to airflow user
USER airflow

# Expose ports
# 8080 - Airflow Web UI
# 5432 - PostgreSQL (if using as metadata DB)
# 1433 - SQL Server
EXPOSE 8080 5432 1433

# Health check for Airflow webserver
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')"

# Default command - start Airflow webserver and scheduler
CMD ["bash", "-c", "airflow webserver --port 8080 & airflow scheduler"]
