"""project_pyamp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^templates/(?P<tmpl_name>\w+)$', views.template, name='template'),
    url(r'^api/checkout$', views.CheckOut.as_view(), name='checkout'),
    url(r'^api/truck/(?P<pk>\w+)?$', views.TruckList.as_view(), name='truck'),
    url(r'^api/truck/(?P<truck_id>\d+)/items?$', views.ItemsInTruck.as_view(), name='truck'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
