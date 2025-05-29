import sqlite3
from typing import Optional, Dict, List
from contextlib import contextmanager
from config.settings import Config
from core.logger import setup_logger

logger = setup_logger("database")

@contextmanager
def db_connection():
    """Context manager for database connections."""
    conn = None
    try:
        conn = sqlite3.connect(Config.DATABASE_FILE)
        conn.row_factory = sqlite3.Row
        yield conn
    except sqlite3.Error as e:
        logger.error(f"Database error: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()

def init_db() -> bool:
    """Initialize the database."""
    try:
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trades (
                    id TEXT PRIMARY KEY,
                    price REAL NOT NULL,
                    quantity REAL NOT NULL,
                    type TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    usd_value REAL GENERATED ALWAYS AS (price * quantity) VIRTUAL
                )
            """)
            conn.commit()
            return True
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        return False

def save_trade(trade_data: Dict) -> bool:
    """Save trade data to database."""
    required_fields = {'id', 'price', 'quantity'}
    if not all(field in trade_data for field in required_fields):
        logger.error("Trade data missing required fields")
        return False

    try:
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO trades (id, price, quantity, type)
                VALUES (?, ?, ?, ?)
            """, (
                trade_data['id'],
                trade_data['price'],
                trade_data['quantity'],
                trade_data.get('type')
            ))
            conn.commit()
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        logger.error(f"Failed to save trade: {str(e)}")
        return False

def get_filtered_trades(
    min_volume: Optional[float] = None,
    min_usd: Optional[float] = None,
    limit: int = 100
) -> List[Dict]:
    """Retrieve filtered trades from database."""
    try:
        with db_connection() as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM trades"
            conditions = []
            params = []
            
            if min_volume is not None:
                conditions.append("quantity >= ?")
                params.append(min_volume)
                
            if min_usd is not None:
                conditions.append("usd_value >= ?")
                params.append(min_usd)
                
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
                
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
            
    except sqlite3.Error as e:
        logger.error(f"Failed to retrieve trades: {str(e)}")
        return []