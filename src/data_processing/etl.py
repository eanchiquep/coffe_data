import pandas as pd
import logging
from config.settings import DATA_PATH, LOGS_PATH

logger = logging.getLogger(__name__)


def load_data(filename):
    """Load data from file"""
    try:
        filepath = DATA_PATH / filename
        if filename.endswith('.csv'):
            df = pd.read_csv(filepath)
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(filepath)
        else:
            raise ValueError(f"Unsupported file format: {filename}")
        logger.info(f"Loaded {filename}: {len(df)} rows")
        return df
    except Exception as e:
        logger.error(f"Failed to load {filename}: {e}")
        raise


def save_data(df, filename):
    """Save processed data to file"""
    try:
        filepath = DATA_PATH / filename
        if filename.endswith('.csv'):
            df.to_csv(filepath, index=False)
        elif filename.endswith('.xlsx'):
            df.to_excel(filepath, index=False)
        else:
            raise ValueError(f"Unsupported file format: {filename}")
        logger.info(f"Saved {filename}: {len(df)} rows")
    except Exception as e:
        logger.error(f"Failed to save {filename}: {e}")
        raise


def validate_data(df, required_columns=None):
    """Validate data quality"""
    if df.empty:
        logger.warning("DataFrame is empty")
        return False
    
    if required_columns:
        missing = set(required_columns) - set(df.columns)
        if missing:
            logger.error(f"Missing columns: {missing}")
            return False
    
    logger.info(f"Data validation passed: {len(df)} rows, {len(df.columns)} columns")
    return True
