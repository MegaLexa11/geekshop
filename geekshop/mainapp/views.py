import random

from django.shortcuts import render, get_object_or_404
from mainapp.models import Product, ProductCategory
from basketapp.models import Basket
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
        return Basket.objects.filter(user=user)
    return 0


def links():
    return ProductCategory.objects.filter(is_active=True)


def hot_product():
    return random.sample(list(Product.objects.exclude(is_active=False)), 1)[0]


def same_hot_products():
    return Product.objects.filter(category__pk=hot_product().pk).order_by('price').exclude(pk=hot_product().pk)


def products(request, pk=None, page=1):
    title = 'продукты'

    if pk is not None:
        if pk == 0:
            category = {
                'name': 'все',
                'pk': 0,
            }
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')

        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'links_menu': links(),
            'title': title,
            'products': products_paginator,
            'category': category,
            'basket': get_basket(user=request.user)
        }

        return render(request, 'mainapp/products_list.html', context)

    context = {
        'links_menu': links(),
        'title': title,
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
