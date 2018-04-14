from django.urls import path

from .views import Home, test

urlpatterns = [
    path('test/', test, name='test'),
    path('', Home.as_view(), name='home'),
]
