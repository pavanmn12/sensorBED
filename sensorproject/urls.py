"""sensorproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from sensorapp.views import *
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^sensor-data/((?P<pk>\d+)/)*$', SensorDataAPI.as_view()),
    url(r'^sensor-data-list/', ListingAPIs.as_view({'get': 'sensor_data_list'})),
    url(r'^filter-sensor-data/', ListingAPIs.as_view({'post': 'filter_sensor_data'}))
]
