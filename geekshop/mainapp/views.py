import random

from django.shortcuts import render, get_object_or_404
from mainapp.models import Product, ProductCategory
from basketapp.models import Basket


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


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter()
    return 0


def links():
    return ProductCategory.objects.all()


def hot_product():
    return random.sample(list(Product.objects.all()), 1)[0]


def same_hot_products():
    return Product.objects.filter(category__pk=hot_product().pk).order_by('price').exclude(pk=hot_product().pk)


def products(request, pk=None):

    if pk:
        if pk == 0:
            products = Product.objects.all()
            category = {
                'name': 'все',
                'pk': 0,
            }
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        context = {
            'links_menu': links(),
            'title': 'Продукты',
            'products': products,
            'category': category,
            'basket': get_basket(user=request.user)
        }

        return render(request, 'mainapp/products_list.html', context)

    context = {
        'links_menu': links(),
        'title': 'Продукты',
        'hot_product': hot_product(),
        'same_products': same_hot_products(),
        'basket': get_basket(user=request.user)
    }

    return render(request, 'mainapp/products.html', context=context)


def product(request, pk):

    context = {
        'title': 'Продукты',
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(user=request.user),
        'links_menu': links(),
    }

    return render(request, 'mainapp/product.html', context=context)
