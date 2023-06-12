"""
URL configuration for netcars project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('manuf_data/', views.get_manuf_json, name = 'car_data' ),
    path('model_data/<str:manuf>/', views.get_model_json, name = 'model_data'),
    path('read_car/', views.get_car_param, name = 'param_list'),
    path('price_car/', views.get_OCT, name = 'price_list'),
    path('test_car/', views.testTest, name = 'test'),
    path('options_car/', views.getOptions, name = 'options'),
    path('filters_car/', views.getParams, name = 'filters')
]
urlpatterns += staticfiles_urlpatterns()