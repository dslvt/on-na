from django.shortcuts import render
from django.http import JsonResponse
from bs4 import BeautifulSoup as bf
import urllib3
import numpy as np

def index(request):
    context = {}
    return render(request, 'kv/home.html', context)

def market(request):
    soup = get_html_from_avito()
    data = {
        'std': round(get_market_std(soup)),
        'mean': round(get_market_mean(soup)),
        'n': round(get_market_n(soup))
    }
    return JsonResponse(data)

def get_market_std(soup):
    money = [money_prepros(d) for d in get_money(soup)]
    train_x = np.array(money).astype(np.float64)
    return train_x.std()

def get_market_mean(soup):
    money = [money_prepros(d) for d in get_money(soup)]
    train_x = np.array(money).astype(np.float64)
    return train_x.mean()

def get_market_n(soup):
    money = [money_prepros(d) for d in get_money(soup)]
    train_x = np.array(money).astype(np.float64)
    return (len(train_x))

def get_html_from_avito():
    http = urllib3.PoolManager()
    answer = ''
    r = http.request('GET', 'https://www.avito.ru/rossiya/kvartiry/prodam?pmax=5000000&pmin=0&s_trg=4&f=549_5696-5697-5698-5699.59_13990b.497_5185b ')
    soup = bf(r.data, 'html.parser')
    return soup

def get_money(soup):
    return [price.text for price in soup.find_all('span', {"class": "price"})]

def money_prepros(req):
    return req.replace(' ', '').replace('\n', '').replace('₽', '')
