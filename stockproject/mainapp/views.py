from django.http import HttpResponse
from django.shortcuts import render
from yahoo_fin.stock_info import *
import pandas as pd
import time
import queue
from threading import Thread
# Create your views here.

def stockPicker(request):
    stock_picker = tickers_nifty50()
    print(stock_picker)
    return render(request, 'mainapp/stockpicker.html', {'stockpicker':stock_picker})
def my_get_quote_table(symbol):
    site = f'https://finance.yahoo.com/quote/{symbol}?p={symbol}&.tsrc=fin-srch'

    # Define headers to simulate a user agent (optional but recommended)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Make the HTTP request and read HTML tables
    tables = pd.read_html(requests.get(site, headers=headers).text)

    # Concatenate the tables into a single DataFrame
    data = pd.concat(tables, ignore_index=True)

    return data
def stockTracker(request):

    stockpicker = request.GET.getlist('stockpicker')
    data = {}

    available_stocks = tickers_nifty50()
    for i in stockpicker:
        if i in available_stocks:
            # details = my_get_quote_table(i)
            pass
        else:
            return HttpResponse("Error")
    
    n_threads = len(stockpicker)
    thread_list = []
    que = queue.Queue()
    start = time.time()
    
    for i in range(n_threads):
        thread = Thread(target=lambda q, arg1: q.put({stockpicker[i]: my_get_quote_table(arg1).to_dict()}), args=(que, stockpicker[i]))
        thread_list.append(thread)
        thread_list[i].start()
    
    for thread in thread_list:
        thread.join()
    
    while not que.empty():
        result = que.get()
        data.update(result)

    end = time.time()
    time_taken  = end - start


    
    restructured_data = {}

    for stock_symbol, stock_data in data.items():
        key_values = stock_data[0]
        key_data = stock_data[1]

        stock_info = {key_values[i]: key_data[i] for i in range(len(key_values))}
        restructured_data[stock_symbol] = [stock_info]

    for stock_symbol, stock_data in data.items():
        key_values = stock_data[0]
        key_data = stock_data[1]

        stock_info = {key_values[i].replace(' ', ''): key_data[i] for i in range(len(key_values))}
        restructured_data[stock_symbol] = [stock_info]


    headers = list(restructured_data[next(iter(data))][0])
    
    

    context = {
        'data':restructured_data,
        'headers':headers
    }
    print(context)

    return render(request, 'mainapp/stocktracker.html', context)


