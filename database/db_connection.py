"""
Module for managing database connections.
"""

import logging
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DatabaseConnection:
    """Manages the SQLAlchemy database connection."""
    
    _engine = None
    
    @classmethod
    def get_engine(cls) -> Engine:
        """
        Returns a cached SQLAlchemy engine.
        
        Returns:
            Engine: The SQLAlchemy engine.
        """
        if cls._engine is None:
            # Using mysql-connector-python dialect
            if DB_PASSWORD:
                connection_string = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            else:
                connection_string = f"mysql+mysqlconnector://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
                
            cls._engine = create_engine(
                connection_string,
                pool_pre_ping=True,  # prevents stale connection errors
                echo=False
            )
            logging.info(f"Created new SQLAlchemy engine for {DB_HOST}:{DB_PORT}/{DB_NAME}")
            
        return cls._engine
        
    @classmethod
    def test_connection(cls):
        """Test the database connection with a simple SELECT 1."""
        engine = cls.get_engine()
        try:
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1")).scalar()
                if result == 1:
                    logging.info("Database connection test successful (SELECT 1 returned 1).")
                else:
                    logging.error("Database connection test failed: unexpected result.")
        except Exception as e:
            logging.error(f"Database connection test failed with exception: {e}")
            raise

if __name__ == "__main__":
    DatabaseConnection.test_connection()
