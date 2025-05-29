from flask import Flask, render_template, request
from datetime import datetime
from core.filters import get_filtered_trades
from config.settings import Config
from core.logger import setup_logger

logger = setup_logger("web_app")

app = Flask(__name__,
            template_folder="templates",
            static_folder="static")
app.secret_key = Config.FLASK_SECRET_KEY

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

@app.route('/')
def index():
    try:
        min_volume = request.args.get('min_volume', type=float)
        min_usd = request.args.get('min_usd', type=float)
        
        trades = get_filtered_trades(
            min_volume=min_volume,
            min_usd=min_usd,
            limit=100
        )
        
        return render_template(
            "index.html",
            trades=trades,
            filters={
                'min_volume': min_volume,
                'min_usd': min_usd
            }
        )
    except Exception as e:
        logger.error(f"Index route error: {e}")
        return render_template("error.html", error=str(e)), 500

if __name__ == '__main__':
    app.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT)