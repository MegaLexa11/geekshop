from django.urls import path
from basketapp import views as basketapp

app_name = 'basketapp'

urlpatterns = [
    path('', basketapp.basket, name='basket'),
    path('add/<int:pk>/', basketapp.add, name='add'),
    path('remove/<int:pk>/', basketapp.remove, name='remove'),
]
