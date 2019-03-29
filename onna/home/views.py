from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse


def index(request):
    context = {}
    return render(request, 'home/home.html', context)

def query(request):
    qr = request.GET.get('query', None)
    data = {
        'is_taken':True
    }
    return JsonResponse(data)
