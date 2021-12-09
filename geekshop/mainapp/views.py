import random

from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.list import ListView
from mainapp.models import Product, ProductCategory


def main(request):
    context = {
        'title': 'Главная',
        'products': Product.objects.all()[:4],
    }
    return render(request, 'mainapp/index.html', context=context)


def contact(request):
    context = {
        'title': 'Контакты'
    }
    return render(request, 'mainapp/contact.html', context=context)


def links():
    return ProductCategory.objects.filter(is_active=True)


class HotProductDetailView(DetailView):
    model = Product
    template_name = 'mainapp/products.html'

    def get_object(self, queryset=None):
        return random.sample(list(Product.objects.exclude(is_active=False)), 1)[0]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['same_products'] = Product.objects.filter(category=self.object.category, is_active=True).\
            order_by('price').exclude(pk=self.object.pk)
        context['links_menu'] = links()
        context['title'] = 'Продукты'
        return context


class ProductsListView(ListView):
    template_name = 'mainapp/products_list.html'
    model = Product
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)
        category_pk = self.kwargs.get('pk')
        if category_pk != 0:
            queryset = queryset.filter(category__pk=category_pk, is_active=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        category_pk = self.kwargs.get('pk')
        context['links_menu'] = links()
        context['title'] = 'Продукты'
        if category_pk == 0:
            context['category'] = {
                'name': 'все',
                'pk': 0,
            }
        else:
            context['category'] = ProductCategory.objects.get(pk=category_pk)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'mainapp/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Продукты'
        context['links_menu'] = links()
        return context
