from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from bs4 import BeautifulSoup as bf
import urllib3
import numpy as np
from sklearn.metrics import r2_score
import xlwt
from datetime import datetime
from django.conf import settings as djangoSettings
from django.core.files.storage import FileSystemStorage
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import os
from django.conf import settings



def index(request):
    context = multiple_params
    return render(request, 'home/home.html', context)

def query(request):
    qr = {
        'mark':request.GET.get('mark', None),
        'model':request.GET.get('model', None),
        'year':request.GET.get('year', None),
        'engine':request.GET.get('engine', None),
        'millage':request.GET.get('millage', None),
        'kpp':request.GET.get('kpp', None),
    }
    soup = get_html_from_avito(qr)
    data = {
        'std': round(get_market_std(soup)),
        'mean': round(get_market_mean(soup)),
        'n': round(get_market_n(soup))
    }
    return JsonResponse(data)

def report(request):
    qr = {
        'mark':request.GET.get('mark', None),
        'model':request.GET.get('model', None),
        'year':request.GET.get('year', None),
        'engine':request.GET.get('engine', None),
        'millage':request.GET.get('millage', None),
        'kpp':request.GET.get('kpp', None),
        'u_price':request.GET.get('u_price', None),
        'u_mileage':request.GET.get('u_mileage', None),
        'u_year':request.GET.get('u_year', None),
        'u_eng':request.GET.get('u_eng', None),
        'u_h_power':request.GET.get('u_h_power', None)
    }
    soup = get_html_from_avito(qr)
    train_x = create_train_data(soup)
    user_data = [0, qr['u_price'], qr['u_mileage'], qr['u_year'], 0,1,0,qr['u_eng'],qr['u_h_power']]
    data = {
        'multi_r': round(get_coor_coef(train_x, user_data)),
        'r_sqr': round(get_r_sq(train_x, user_data)),
        'norm_r': round(get_norm_r(train_x, user_data)),
        'std': round(np.array(train_x).astype(np.float64).std()),
        'n': round(len(train_x))
    }
    tdata = {'url':create_xls(qr,data,soup)}
    return JsonResponse(tdata)

def create_xls(qr,data,soup):

    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
        num_format_str='#,##0.00')
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

    wb = xlwt.Workbook()
    ws = wb.add_sheet('Report analogs')

    reg_labes = ["Регрессионная статистика", "Множественный R", "R-квадрат", "Нормированный R-квадрат", "Стандартная ошибка", "Наблюдения", "Аналоги"]
    for i in range(len(reg_labes)):
        ws.write(i, 0, reg_labes[i])
    ws.write(1,1,data['multi_r'])
    ws.write(2,1,data['r_sqr'])
    ws.write(3,1,data['norm_r'])
    ws.write(4,1,data['std'])
    ws.write(5,1,data['n'])

    rows_info = get_date(soup)
    mark = qr['mark']
    model = qr['model']

    labes = ["#", "Mark", "Model", "Year", "Engine volume", "Mileage", "kpp", "Horse powers", 'is_bitaya', "url"]
    #is_brouken,money[i],km,year[i], at,mt,amt,engine_v,house_power
    for i in range(len(labes)):
        ws.write(7, i, labes[i])
    for i in range(len(rows_info)):
        ws.write(8+i, 0, i+1)
        ws.write(8+i, 1, mark)
        ws.write(8+i, 2, model)
        ws.write(8+i, 3, rows_info[i][3])
        ws.write(8+i, 4, rows_info[i][7])
        ws.write(8+i, 5, rows_info[i][2])
        cur_kpp = 'MT'
        if rows_info[i][4]==1:
            rows_info[i][4] = 'AT'
        if rows_info[i][5]==1:
            rows_info[i][5] = 'MT'
        if rows_info[i][6]==1:
            rows_info[i][6] = 'AMT'
        ws.write(8+i, 6, cur_kpp)
        ws.write(8+i, 7, rows_info[i][8])
        ws.write(8+i, 8, rows_info[i][9])
    file_location = './media/report.xls'
    wb.save(file_location)
    print(os.path.join(settings.MEDIA_ROOT, 'report.xls'))
    return os.path.join(settings.MEDIA_ROOT, 'report.xls')

def get_date(soup):
    raw_data = [preparsing(d) for d in get_data(soup)]
    x_money = [money_prepros(d) for d in get_money(soup)]
    x_year = [year_prepros(d) for d in get_year(soup)]
    urls = get_url(soup)
    pre_data = create_train_x(x_money,x_year, raw_data)
    new_shit = []
    for i in range(len(urls)):
        new_shit.append(pre_data[i])
        new_shit[-1].append(urls[i])

    return new_shit

def create_train_data(soup_in):
    raw_data = [preparsing(d) for d in get_data(soup_in)]
    x_money = [money_prepros(d) for d in get_money(soup_in)]
    x_year = [year_prepros(d) for d in get_year(soup_in)]
    train_x = create_train_x(x_money, x_year, raw_data)
    return train_x

def product(request):
    qr = {
        'mark':request.GET.get('mark', None),
        'model':request.GET.get('model', None),
        'year':request.GET.get('year', None),
        'engine':request.GET.get('engine', None),
        'millage':request.GET.get('millage', None),
        'kpp':request.GET.get('kpp', None),
        'u_price':request.GET.get('u_price', None),
        'u_mileage':request.GET.get('u_mileage', None),
        'u_year':request.GET.get('u_year', None),
        'u_eng':request.GET.get('u_eng', None),
        'u_h_power':request.GET.get('u_h_power', None)
    }
    soup = get_html_from_avito(qr)
    train_x = create_train_data(soup)
    user_data = [0, qr['u_price'], qr['u_mileage'], qr['u_year'], 0,1,0,qr['u_eng'],qr['u_h_power']]
    data = {
        'multi_r': round(get_coor_coef(train_x, user_data)),
        'r_sqr': round(get_r_sq(train_x, user_data)),
        'norm_r': round(get_norm_r(train_x, user_data)),
        'std': round(np.array(train_x).astype(np.float64).std()),
        'n': round(len(train_x))
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

def get_url(soup):
    base = 'https://www.avito.ru'
    return [base + price['href'] for price in soup.find_all('a', {"class":"item-description-title-link"}, href=True)]

def money_prepros(req):
    return req.replace(' ', '').replace('\n', '').replace('₽', '')
def year_prepros(req):
    return req.split(',')[1].replace(' ','')
def preparsing(shit):
    return [st.replace('\xa0', ' ').replace('\n', '').replace(' ', '') for st in shit.split(',')]

def create_train_x(x_money, x_year, request):
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
    coor = np.corrcoef(np.array(train_x).astype(np.float), np.array(train_y).astype(np.float))
    return np.array([coor[i][-1] for i in range(len(coor))]).mean()

def get_r_sq(train_x, train_y):
    scores = [r2_score(np.array(train_y).astype(np.float64), np.array(train_x[i]).astype(np.float64)) for i in range(len(train_x))]
    return sum(scores)/len(scores)

def get_norm_r(train_x ,user_data):
    r = get_coor_coef(train_x, user_data)
    n = len(train_x)
    p = len(train_x)-len(train_x[0])
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
