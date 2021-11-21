"""
Definition of views.
"""

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from django.contrib.auth.forms import UserCreationForm

from app.forms import CommentForm

from .models import Cart, Comment, Order, Product

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'year':datetime.now().year,
        }
    )

def news(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/news.html',
        {
            'title':'Новости',
            'year':datetime.now().year,
        }
    )

def catalog(request):
    """Renders the about page."""
    products = Product.objects.all().order_by('price')
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/catalog.html',
        {
            'title': 'Товары',
            'products': products,
            'year':datetime.now().year,
            }
        )

def registration(request):
    """Renders the registration page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST": # после отправки формы
        regform = UserCreationForm (request.POST)
        if regform.is_valid(): #валидация полей формы
            reg_f = regform.save(commit=False) # не сохраняем автоматически данные формы
            reg_f.is_staff = False # запрещен вход в административный раздел
            reg_f.is_active = True # активный пользователь
            reg_f.is_superuser = False # не является суперпользователем
            reg_f.date_joined = datetime.now() # дата регистрации
            reg_f.last_login = datetime.now() # дата последней авторизации
            reg_f.save() # сохраняем изменения после добавления данных
            return redirect('home') # переадресация на главную страницу после регистрации
    else:
        regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform, # передача формы в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )

def product(request, parametr):
    """Renders the about page."""
    try:
        product = Product.objects.get(product_id = parametr)
    except Product.DoesNotExist:
        product = None

    try:
        comments = Comment.objects.filter(product = product)
    except Comment.DoesNotExist:
        comments = None

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit = False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.product = Product.objects.get(product_id = parametr)
            comment_f.save()

            return redirect('product', parametr = product.product_id)
    else: 
        form = CommentForm()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/product.html',
        {
            'product': product,
            'comments': comments,
            'form': form,
            'title':'Товар',
            'year':datetime.now().year,
        }
    )

def managerOrders(request):
    """Renders the about page."""

    querySum = 'select o.id, o.client_id as clientID, o.order_id as orderID, sum(p.price) as totalSum from Products as p join Orders as o on o.product_id = p.id group by o.order_id'

    queryOrders = 'select p.id, o.order_id as orderID, o.client_id as clientID, p.product_id as productID, p.name as productName, p.price as priceForProduct, count(p.id) as countOfProduct, sum(p.price) as sumForCount from Orders AS o join Products as p on o.product_id = p.id group by p.id, o.order_id'

    orders = Order.objects.raw(queryOrders)
    # Нужные поля объекта:
    # orderID - номер заказа
    # clientID - id клиента (из таблицы заказов) ? мб не нужно
    # productID - id продукта (pdoduct_id из Product, не id из таблицы)
    # productName - имя продукта
    # priceForProduct - цена за единицу
    # countOfProduct - количество
    # sumForCount - цена за все количество одного продукта

    sums = Order.objects.raw(querySum)
    # Нужные поля объекта:
    # clientID - id клиента
    # orderID - номер заказа
    # totalSum - общая сумма заказа

    # Есть ли способ лучше написать запросы к бд?..

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/manager-orders.html',
        {
            'sums': sums,
            'orders': orders,
            'title':'Заказы',
            'year':datetime.now().year,
        }
    )

def clientCart(request):

    carts = Cart.objects.filter(client = request.user.id)

    totalSum = 0
    for cart in carts:
        totalSum += cart.product.price

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/client-cart.html',
        {
            'totalSum': totalSum,
            'carts': carts,
            'title':'Корзина',
            'year':datetime.now().year,
        }
    )

def clientOrders(request):

    if not request.user.is_staff and not request.user.is_superuser:
        orders = Order.objects.filter(client = request.user.id)
        totalSum = 0
        for order in orders:
            totalSum += order.product.price

    else:
        orders = Order.objects.get()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/client-orders.html',
        {
            'totalSum': totalSum,
            'orders': orders,
            'title':'Заказы',
            'year':datetime.now().year,
        }
    )