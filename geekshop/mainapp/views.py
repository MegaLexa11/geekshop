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
        return sum(list(Basket.objects.filter(user=user).values_list('quantity', flat=True)))
    return 0


def get_cost(user):
    if user.is_authenticated:
        cost = 0
        for basket in Basket.objects.filter(user=user):
            cost += basket.product.price * basket.quantity
        return cost
    return 0


def products(request, pk=None):
    basket = get_basket(request.user)
    cost = get_cost(request.user)

    links_menu = ProductCategory.objects.all()

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
            'links_menu': links_menu,
            'title': 'Продукты',
            'products': products,
            'category': category,
            'basket': basket,
            'cost': cost,
        }

        return render(request, 'mainapp/products_list.html', context)

    hot_product = random.sample(list(Product.objects.all()), 1)[0]
    same_products = Product.objects.filter(category=hot_product.category)

    context = {
        'links_menu': links_menu,
        'title': 'Продукты',
        'hot_product': hot_product,
        'same_products': same_products,
        'basket': basket,
        'cost': cost,
    }

    return render(request, 'mainapp/products.html', context=context)
