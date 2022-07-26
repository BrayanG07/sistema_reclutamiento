from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('vacantes', views.vacantes, name='vacantes'),
]

urlpatterns += staticfiles_urlpatterns()