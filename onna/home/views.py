from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse



def index(request):
    context = multiple_params
    return render(request, 'home/home.html', context)

def query(request):
    qr = request.GET.get('query', None)
    data = {
        'is_taken':True
    }
    return JsonResponse(data)







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
