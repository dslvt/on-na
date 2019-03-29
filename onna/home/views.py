from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from bs4 import BeautifulSoup as bf
import urllib3
import numpy as np

def index(request):
    context = multiple_params
    return render(request, 'home/home.html', context)

def query(request):
    qr = request.GET.get('query', None)
    soup = get_html_from_avito(qr)
    data = {
        'std': round(get_market_std(soup)),
        'mean': round(get_market_mean(soup)),
        'n': round(get_market_n(soup))
    }
    return JsonResponse(data)

def report(request):
    qr = request.GET.get('report', None)
    data = {}
    return JsonResponse(data)

def product(request):
    qr = request.GET.get('product', None)
    data = {}
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
    return len(train_x)

def get_html_from_avito(params):
    http = urllib3.PoolManager()
    answer = ''

    avito_url = get_avito_url(params)
    r = http.request('GET', avito_url)
    soup = bf(r.data, 'html.parser')
    return soup

def get_avito_url(prm):
    base = 'https://www.avito.ru/rossiya/avtomobili'
    try:
        base += "/"+ prm['mark']
    except (KeyError, TypeError):
        pass
    try:
        base += '/'+prm['model']
    except (KeyError, TypeError):
        pass
    base += '?s_trg=4&f='
    try:
        base += get_type_range_url('body', prm['body'])
    except (KeyError, TypeError):
        pass
    try:
        base += '.'+get_range_url('year',prm['year'])
    except (KeyError, TypeError):
        pass
    try:
        base += '.'+get_type_range_url('kpp', prm['kpp'])
    except (KeyError, TypeError):
        pass
    try:
        base += '.'+get_range_url('engine', prm['engine'])
    except (KeyError, TypeError):
        pass
    return base

def get_range_url(name, prms):
    base = multiple_params[name]['base']
    all_params = list(multiple_params[name])
    a1, a2=-1,-1
    for pr in all_params:
        if pr != 'base':
            if float(prms[0])<=float(pr):
                a1 = multiple_params[name][pr]
                break
    for pr in all_params:
        if pr != 'base':
            if float(prms[1])<=float(pr):
                a2 = multiple_params[name][pr]
                break
    return str(base)+'_'+str(a1)+'b'+str(a2)

def get_type_range_url(name, prms):
    first, second = multiple_params[name][prms[0]], multiple_params[name][prms[1]]
    base = multiple_params[name]['base']
    return str(base)+'_'+str(first)+'-'+str(second)

def create_reg_anal():
    pass

def get_data(soup):
    return [price.text for price in soup.find_all('div', {"class": "specific-params specific-params_block"})]

def get_money(soup):
    return [price.text for price in soup.find_all('span', {"class": "price"})]

def get_year(soup):
    return [price.text for price in soup.find_all('a', {"class": "item-description-title-link"})]

def money_prepros(req):
    return req.replace(' ', '').replace('\n', '').replace('₽', '')
def year_prepros(req):
    return req.split(',')[1].replace(' ','')
def preparsing(shit):
    return [st.replace('\xa0', ' ').replace('\n', '').replace(' ', '') for st in shit.split(',')]

def create_train_x(money, year, request):
    train_x = []
    for rq in request:
        is_brouken = 0
        km = 0
        at,mt,amt=0,0,0
        house_power = 0
        engine_v = 0
        for i in range(len(rq)):
            if rq[i].find('Битый') != -1:
                is_brouken = 1
            if rq[i].find('км') != -1:
                km = int(rq[i].replace('км', ''))
            if rq[i].find('AT') != -1:
                at=1
            if rq[i].find('MT') != -1:
                mt=1
            if rq[i].find('AMT') != -1:
                amt=1
            if rq[i].find('л.с.') != -1:
                house_power = int(rq[i][rq[i].find('(')+1:rq[i].find('л')])
                engine_v = float(rq[i][rq[i].find('.')-1:rq[i].find('.')+2])
            if x_money[i] == 0 or x_year[i] == 0 or house_power==0 or engine_v==0 or km==0:
                continue
            train_x.append([is_brouken,x_money[i],km,x_year[i], at,mt,amt,engine_v,house_power])
    return train_x

def get_coor_coef(train_x, train_y):
    coor = np.corrcoef(np.array(train_x).astype(np.float), np.array(test_x).astype(np.float))
    return np.array([coor[i][-1] for i in range(len(coor))]).mean()

def get_r_sq(train_x, train_y):
    scores = [r2_score(np.array(test_x).astype(np.float64), np.array(train_x[i]).astype(np.float64)) for i in range(len(train_x))]
    return sum(scores)/len(scores)

def get_norm_r(r, n, p):
    return 1-(1-p)*(n-1)/(n-p-1)




multiple_params = {
   'kpp':{
       'base':185,
       'mechanika':861,
       'avtomat':860,
       'robot':14754,
       'vibator':14753,
       },
    'year':{
        'base':188,
        '1960':0,
        '1970':782,
        '2012':6045,
        '2019':405242,
    },
    'body':{
        'base':187,
        'sedan':869,
        'limusin':867,
        'chechbeck':872
    },
    'engine':{
        'base':1374,
        '0.0':0,
        '0.6':15776,
        '5.5':15825,
        '6.0':15830
    },
    'mark':{
        'skoda':['octavia', 'rapid'],
        'vaz_lada':['kalina', 'granta'],
        'kia':['rio','spectra']
    },
}
