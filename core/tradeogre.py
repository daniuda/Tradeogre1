import requests
from config.settings import Config
from core.logger import setup_logger

logger = setup_logger("tradeogre")

def get_recent_trades(market=None):
    """Fetch recent trades from TradeOgre API"""
    market = market or Config.TRADE_PAIR
    url = f"https://tradeogre.com/api/v1/history/{market}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        trades = response.json()
        
        if not isinstance(trades, list):
            logger.error(f"Unexpected API response: {trades}")
            return []
            
        # Add missing fields and format data
        formatted_trades = []
        for trade in trades:
            formatted_trades.append({
                'id': str(trade.get('date', '')),
                'price': float(trade.get('price', 0)),
                'quantity': float(trade.get('quantity', 0)),
                'type': 'buy' if trade.get('type') == '0' else 'sell',
                'timestamp': trade.get('date', '')
            })
            
        return sorted(formatted_trades, key=lambda x: x['timestamp'], reverse=True)
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return []