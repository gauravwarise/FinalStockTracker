from celery import shared_task
from .views import my_get_quote_table
from yahoo_fin.stock_info import *
from threading import Thread
import queue
import asyncio
from channels.layers import get_channel_layer
import simplejson as json
import numpy as np


@shared_task(bind=True)
def update_stock(self, stockpicker):
    data = {}
    # stockpicker = request.GET.getlist('stockpicker')
    # data = {}

    available_stocks = tickers_nifty50()
    for i in stockpicker:
        if i in available_stocks:
            # details = my_get_quote_table(i)
            pass
        else:
            stockpicker.remove(i)

    n_threads = len(stockpicker)
    thread_list = []
    que = queue.Queue()
    
    for i in range(n_threads):
        # thread = Thread(target=lambda q, arg1: q.put({stockpicker[i]: json.loads(json.dumps(my_get_quote_table(arg1), ignore_nan=True))}), args=(que, stockpicker[i]))
        thread = Thread(target=lambda q, arg1: q.put({stockpicker[i]: my_get_quote_table(arg1).to_dict()}), args=(que, stockpicker[i]))
        thread_list.append(thread)
        thread_list[i].start()
    
    for thread in thread_list:
        thread.join()
    
    while not que.empty():
        result = que.get()
        data.update(result)

    restructured_data = {}

    for stock_symbol, stock_data in data.items():
        key_values = stock_data[0]
        key_data = stock_data[1]

        stock_info = {key_values[i]: key_data[i] for i in range(len(key_values))}
        restructured_data[stock_symbol] = [stock_info]

    for stock_symbol, stock_data in data.items():
        key_values = stock_data[0]
        key_data = stock_data[1]

        key_data = np.nan_to_num(key_data, nan=None)

        stock_info = {key_values[i].replace(' ', ''): key_data[i] for i in range(len(key_values))}
        restructured_data[stock_symbol] = [stock_info]

    #send data to group 
    channel_layer = get_channel_layer()
    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)
    loop.run_until_complete(channel_layer.group_send('stock_track',{
        'type':'send_stock_update',
        'message':restructured_data,
    }))

    return "Done"
