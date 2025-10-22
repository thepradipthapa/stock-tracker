from django.shortcuts import render
import yfinance as yf
import time


# Create your views here.
def stock_list(request):
    # replace with your desired tickers
    tickers = ['AAPL', 'MSFT', 'GOOG', 'NVDA', 'SSNLF', 'AMZN', 'META', 'INTC', 'ORCL', 'IBM',
    'ADBE', 'CSCO', 'TXN', 'CRM', 'AVGO', 'QCOM', 'SAP', 'AMD', 'SONY', 'TWTR',
    'PANW', 'NOW', 'SNPS', 'ANET', 'ZM', 'DOCU', 'SHOP', 'SQ', 'UBER', 'LYFT',
    'TSM', 'NFLX', 'BIDU', 'BABA', 'EBAY', 'BTI', 'SNE', 'LGIH', 'NOK', 'WDC',
    'STX', 'ZS', 'OKTA', 'SPLK', 'TEAM', 'FSLY', 'DDOG', 'CRWD', 'DOCU']
    stocks = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info
        name = info.get('shortName', ticker)  # Use ticker as fallback
        stocks.append({'symbol': ticker, 'name': name})
    context = {'stocks': stocks}
    return render(request, 'core/stock_list.html', context)


def live_stock_tracker(request):
    stock_list = request.GET.getlist('stocks')
    stock_data = []
    for stock in stock_list:
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

    context = {
        'stock_data': stock_data,
        'room_name': 'track'
    }
    return render(request, 'core/live_stock_tracker.html', context)