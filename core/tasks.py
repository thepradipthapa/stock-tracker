from celery import shared_task
import yfinance as yf

@shared_task
def update_stock_data(stocks):
    stock_data = []
    for stock in stocks:
        ticker = yf.Ticker(stock)
        live_data = ticker.fast_info
        stock_data.append({
            'symbol': stock,
            'price': live_data.get('lastPrice'),
            'open': live_data.get('open'),
            'high': live_data.get('dayHigh'),
            'low': live_data.get('dayLow'),
            'prev_close': live_data.get('previousClose'),
            'volume': live_data.get('lastVolume'),
            'market_cap': live_data.get('marketCap')
        })
