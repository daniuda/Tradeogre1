from flask import Flask, render_template
from core.exchanges.tradeogre import TradeOgreExchange
from core.exchanges.probit import ProBitExchange
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/')
def dashboard():
    try:
        exchanges = {
            "TradeOgre": TradeOgreExchange().get_prices() or {},
            "ProBit": ProBitExchange().get_prices() or {}
        }
        return render_template('dashboard.html', exchanges=exchanges)
    except Exception as e:
        app.logger.error(f"Error in dashboard: {str(e)}")
        return "Error loading data", 500