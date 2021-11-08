from django.shortcuts import render, get_object_or_404
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import HttpResponseRedirect
from authapp.forms import ShopUserRegisterForm, ShopUserEditForm
from django.urls import reverse
from adminapp.forms import ProductCategoryEditForm, ProductEditForm


pass_func = lambda u: u.is_superuser


@user_passes_test(pass_func)
def user_create(request):
    title = 'пользователи/создание'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)

        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        user_form = ShopUserRegisterForm()

    context = {
        'title': title,
        'update_form': user_form,
    }

    return render(request, 'adminapp/user_update.html', context=context)


@user_passes_test(pass_func)
def users(request):
    title = 'админка/пользователи'

    users_list = ShopUser.objects.all().order_by('-is_active', 'username')

    context = {
        'title': title,
        'objects': users_list
    }

    return render(request, 'adminapp/users.html', context=context)


@user_passes_test(pass_func)
def user_update(request, pk):
    title = 'пользователи/редактирование'

    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=edit_user)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('adminapp:users'))

    else:
        edit_form = ShopUserEditForm(instance=edit_user)

    context = {
        'title': title,
        'update_form': edit_form
    }

    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(pass_func)
def user_delete(request, pk):
    title = 'пользователи/удаление'

    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('adminapp:users'))

    context = {
        'title': title,
        'object_to_reset': user,
    }

    return render(request, 'adminapp/user_reset.html', context=context)


@user_passes_test(pass_func)
def user_reset(request, pk):
    title = 'пользователи/восстановление'

    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse('adminapp:users'))

    context = {
        'title': title,
        'object_to_reset': user
    }

    return render(request, 'adminapp/user_reset.html', context=context)


@user_passes_test(pass_func)
def category_create(request):
    title = 'категории/создание'

    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, request.FILES)

        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('adminapp:categories'))
    else:
        category_form = ProductCategoryEditForm()

    context = {
        'title': title,
        'update_form': category_form,
    }

    return render(request, 'adminapp/category_update.html', context=context)


@user_passes_test(pass_func)
def categories(request):
    title = 'админка/категории'

    cat_list = ProductCategory.objects.all().order_by('name')

    context = {
        'title': title,
        'objects': cat_list
    }

    return render(request, 'adminapp/categories.html', context=context)


@user_passes_test(pass_func)
def category_update(request, pk):
    title = 'категории/редактирование'

    edit_category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        edit_form = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('adminapp:categories'))

    else:
        edit_form = ProductCategoryEditForm(instance=edit_category)

    context = {
        'title': title,
        'update_form': edit_form
    }

    return render(request, 'adminapp/category_update.html', context)


@user_passes_test(pass_func)
def category_delete(request, pk):
    title = 'категории/удаление'

    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        category.is_active = False
        category.save()
        return HttpResponseRedirect(reverse('adminapp:categories'))

    context = {
        'title': title,
        'object_to_reset': category,
    }

    return render(request, 'adminapp/category_reset.html', context=context)


@user_passes_test(pass_func)
def category_reset(request, pk):
    title = 'категории/восстановление'

    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        category.is_active = True
        category.save()
        return HttpResponseRedirect(reverse('adminapp:categories'))

    context = {
        'title': title,
        'object_to_reset': category,
    }

    return render(request, 'adminapp/category_reset.html', context=context)


@user_passes_test(pass_func)
def product_create(request, pk):
    return None


@user_passes_test(pass_func)
def products(request, pk):
    title = 'админка/продукты'

    category = get_object_or_404(ProductCategory, pk=pk)
    prod_list = Product.objects.filter(category_id=pk).order_by('name')

    context = {
        'title': title,
        'objects': prod_list,
        'category': category,
    }

    return render(request, 'adminapp/products.html', context)


@user_passes_test(pass_func)
def product_read(request, pk):
    return None


@user_passes_test(pass_func)
def product_update(request, pk):
    return None


@user_passes_test(pass_func)
def product_delete(request, pk):
    return None
