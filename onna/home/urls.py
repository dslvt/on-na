from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('query/', views.query, name='query'),
    path('product/', views.product, name=''),
    path('report/', views.report, name='')
]
