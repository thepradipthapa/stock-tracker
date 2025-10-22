from celery import shared_task
import yfinance as yf
from channels.layers import get_channel_layer
import asyncio

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
        print(f"Updated data for :{stock_data}")


    # send data to group
    channel_layer = get_channel_layer()
    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)

    loop.run_until_complete(channel_layer.group_send("stock_track", {
        'type': 'send_stock_update',
        'message': stock_data,
    }))
    
    return 'Stock data updated and sent to WebSocket group.'