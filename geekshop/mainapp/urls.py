from django.urls import path
from mainapp import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.HotProductDetailView.as_view(), name='products'),
    path('category/<int:pk>', mainapp.ProductsListView.as_view(), name='categories'),
    # path('category/<int:pk>/page/<int:page>', mainapp.products, name='page'),
    path('product/<int:pk>', mainapp.ProductDetailView.as_view(), name='product')
]
