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
    print("=====", stockpicker)
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
    # for i in stockpicker:
    #     result = my_get_quote_table(i)
    #     data.update({i:result.to_dict()})
    for i in range(n_threads):
        thread = Thread(target=lambda q, arg1: q.put({stockpicker[i]: my_get_quote_table(arg1).to_dict()}), args=(que, stockpicker[i]))
        print(thread)
        thread_list.append(thread)
        thread_list[i].start()
    
    for thread in thread_list:
        thread.join()
    
    while not que.empty():
        result = que.get()
        data.update(result)

    end = time.time()
    time_taken  = end - start
    print(time_taken)
    print("================================================")
    print(data)
    print("================================================")

    extracted_data = []

    # Loop through the dictionaries and extract all values
    keys_to_extract = [
    'Previous Close', 'Open', 'Bid', 'Ask',
    "Day's Range", '52 Week Range', 'Volume',
    'Avg. Volume', 'Market Cap', 'Beta (5Y Monthly)',
    'PE Ratio (TTM)', 'EPS (TTM)', 'Earnings Date',
    'Forward Dividend & Yield', 'Ex-Dividend Date',
    '1y Target Est']
    
    formatted_data = {}
    for ticker, stock_data in data.items():
        formatted_data[ticker] = [{column: details[column] for column in details} for details in stock_data.values()]


    print("======================================.....................")
    print(formatted_data)
    print("======================================.....................")

    # details = get_quote_table('RELIANCE.NS')
    # print("================================================")
    # details_dict = details.to_dict()
    # print(details_dict)
    # print("================================================")
    # details_df = pd.DataFrame(details)
    # print(details_df)
    # # print(details)
    # return render(request, 'mainapp/stocktracker.html', {'details': details_df})
    return render(request, 'mainapp/stocktracker.html', {'data': data, 'headers':header_list})



# {"ADANIENT.NS": {0: {0: "Previous Close", 1: "Open", 2: "Bid", 3: "Ask", 4: "Day's Range", 5: "52 Week Range", 6: "Volume", 7: "Avg. Volume", 8: "Market Cap", 9: "Beta (5Y Monthly)", 10: "PE Ratio (TTM)", 11: "EPS (TTM)", 12: "Earnings Date", 13: "Forward Dividend & Yield", 14: "Ex-Dividend Date", 15: "1y Target Est"}, 1: {0: "2205.90", 1: "2205.90", 2: "2,208.55 x 0", 3: "2,209.65 x 0", 4: "2,201.00 - 2,237.95", 5: "1,017.45 - 4,190.00", 6: "745392", 7: "2959299", 8: "2.518T", 9: "0.74", 10: "103.22", 11: "21.40", 12: "Feb 12, 2024 - Feb 16, 2024", 13: "1.20 (0.05%)", 14: "Jul 07, 2023", 15: nan}}, "APOLLOHOSP.NS": {0: {0: "Previous Close", 1: "Open", 2: "Bid", 3: "Ask", 4: "Day"s Range", 5: "52 Week Range", 6: "Volume", 7: "Avg. Volume", 8: "Market Cap", 9: "Beta (5Y Monthly)", 10: "PE Ratio (TTM)", 11: "EPS (TTM)", 12: "Earnings Date", 13: "Forward Dividend & Yield", 14: "Ex-Dividend Date", 15: "1y Target Est"}, 1: {0: "5338.75", 1: "5332.20", 2: "5,477.20 x 0", 3: "5,477.15 x 0", 4: "5,306.15 - 5,493.35", 5: "4,123.00 - 5,493.35", 6: "616981", 7: "419706", 8: "787.439B", 9: "0.58", 10: "112.73", 11: "48.58", 12: "Feb 12, 2024 - Feb 16, 2024", 13: "15.00 (0.28%)", 14: "Aug 18, 2023", 15: "4426.63"}}}

# {
#   'BAJAJ-AUTO.NS': [
#       {
#      'Previous Close':'5550.90',
#      'Open':'5550.90',
#      'Bid':'5,638.55 x 0',
#      'Ask':'5,638.75 x 0',
#      "Day's Range":'5,479.35 - 5,674.95',
#      '52 Week Range':'3,520.05 - 5,674.95'
#      'Volume':'479807',
#      'Avg. Volume':'445316',
#      'Market Cap':'1.596T',
#      'Beta (5Y Monthly)':'0.83',
#        'PE Ratio (TTM)':'23.30',
#        'EPS (TTM)':'242.02',
#        'Earnings Date':'Jan 23, 2024 - Jan 27, 2024',
#        'Forward Dividend & Yield':'140.00 (2.52%)',
#        'Ex-Dividend Date':'Jun 30, 2023'
#        '1y Target Est':'4226.76'
#     }
#   ],

# 'APOLLOHOSP.NS': [
#       {
#      'Previous Close':'2205.90',
#      'Open':'2205.90',
#      'Bid':'0.00 x 0',
#      'Ask':'0.00 x 0',
#      "Day's Range":'2,201.00 - 2,237.95',
#      '52 Week Range':'1,017.45 - 4,190.00',
#      'Volume':'916297',
#      'Avg. Volume':'2959299',
#      'Market Cap':'2.518T',
#      'Beta (5Y Monthly)':'0.74',
#        'PE Ratio (TTM)':'103.21',
#        'EPS (TTM)':'21.40',
#        'Earnings Date':'Feb 12, 2024 - Feb 16, 2024',
#        'Forward Dividend & Yield':'1.20 (0.05%)',
#        'Ex-Dividend Date':'Jul 07, 2023'
#        '1y Target Est':'nan'
#     }
#   ],
#   'ADANIENT.NS': [
#       {
#      'Previous Close':'2205.90',
#      'Open':'2205.90',
#      'Bid':'0.00 x 0',
#      'Ask':'0.00 x 0',
#      "Day's Range":'2,201.00 - 2,237.95',
#      '52 Week Range':'1,017.45 - 4,190.00',
#      'Volume':'916297',
#      'Avg. Volume':'2959299',
#      'Market Cap':'2.518T',
#      'Beta (5Y Monthly)':'0.74',
#        'PE Ratio (TTM)':'103.21',
#        'EPS (TTM)':'21.40',
#        'Earnings Date':'Feb 12, 2024 - Feb 16, 2024',
#        'Forward Dividend & Yield':'1.20 (0.05%)',
#        'Ex-Dividend Date':'Jul 07, 2023'
#        '1y Target Est':'nan'
#     }
#   ]
#   }