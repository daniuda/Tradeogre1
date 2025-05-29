# core/filters.py
import logging
from typing import List, Dict, Optional
from config.settings import Config
from core.database import get_filtered_trades as db_get_filtered_trades
from core.logger import setup_logger

logger = setup_logger("filters")

def apply_filters(
    min_volume: Optional[float] = None,
    min_usd: Optional[float] = None,
    trade_type: Optional[str] = None,
    limit: int = 100
) -> List[Dict]:
    """
    Apply filters to trades and return filtered results
    Args:
        min_volume: Minimum trade volume in base currency
        min_usd: Minimum trade value in USD
        trade_type: Filter by 'buy' or 'sell'
        limit: Maximum number of trades to return
    Returns:
        List of filtered trade dictionaries
    """
    try:
        # Convert None values to defaults from config if not specified
        if min_volume is None:
            min_volume = Config.MIN_VOLUME
        if min_usd is None:
            min_usd = Config.MIN_USD_VALUE

        # Get filtered trades from database
        trades = db_get_filtered_trades(
            min_volume=min_volume,
            min_usd=min_usd,
            limit=limit
        )

        # Additional type filtering if specified
        if trade_type:
            trades = [t for t in trades if t.get('type') == trade_type.lower()]

        logger.debug(f"Returning {len(trades)} filtered trades")
        return trades

    except Exception as e:
        logger.error(f"Error applying filters: {str(e)}")
        return []

# Alias for backward compatibility
get_filtered_trades = apply_filters