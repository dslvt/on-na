from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from bs4 import BeautifulSoup as bf
import urllib3


def index(request):
    context = multiple_params
    return render(request, 'home/home.html', context)

def query(request):
    qr = request.GET.get('query', None)
    print(qr)
    data = {
        'response':get_data_from_avito(qr)
    }
    return JsonResponse(data)

def get_data_from_avito(params):
    http = urllib3.PoolManager()
    answer = ''

    avito_url = get_avito_url(params)
    r = http.request('GET', avito_url)
    soup = bf(r.data, 'html.parser')
    answer = len([price.text for price in soup.find_all('span', {"class": "price"})])
    return answer

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
