from django.urls import path
from ordersapp import views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.OrdersListView.as_view(), name='list'),
    path('create/', ordersapp.OrdersCreateView.as_view(), name='create'),
    path('update/<int:pk>', ordersapp.OrderUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', ordersapp.OrderDeleteView.as_view(), name='delete'),
    path('read/<int:pk>', ordersapp.OrderDetailView.as_view(), name='read'),
    path('cancel/forming/<int:pk>', ordersapp.forming_complete, name='forming_cancel')
]