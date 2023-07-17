from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from main.models import Product


def index(request):
    """Главная страница с товарами"""
    product_list = Product.objects.all()
    items_per_page = 3
    paginator = Paginator(product_list, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'title': 'Главная'
    }

    return render(request, 'main/index.html', context)


def contact(request):
    """Страница с контактным данными"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f' {name} ({email}): {message}')

    context = {
        'title': 'Контакты'
    }

    return render(request, 'main/contact.html', context)


def product(request, pk):
    """Страница с детальным описанием продукта"""
    product_detail = get_object_or_404(Product, pk=pk)

    context = {
        'product_detail': product_detail,
        'desired_id': pk
    }

    return render(request, 'main/product.html', context)
