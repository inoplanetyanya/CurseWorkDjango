"""
Definition of views.
"""

from django.contrib.auth.models import User
from django.db.models import query
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from django.contrib.auth.forms import UserCreationForm

from app.forms import CommentForm

from .models import Cart, Comment, Order, Product

import random

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

    client = User.objects.get(id = request.user.id)

    queryCart = 'select c.client_id, c.product_id, c.product_name from Carts as c'

    carts = Cart.objects.filter(client = client)

    # print('\n\n\t\t\t---Клиент: ', client.query, '\n')
    # print('\n\n\t\t\t---Корзина: ', carts.query, '\n')

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

def addToCart(request, parametr):
    product = Product.objects.get(id = parametr)
    client = User.objects.get(id = request.user.id)
    Cart.objects.create(product = product, client = client)

    return redirect('client-cart')

def removeFromCart(request, parametr):
    cart = Cart.objects.get(id = parametr)
    cart.delete()

    return redirect('client-cart')

def makeOrders(request, parametr):
    client = User.objects.get(id = request.user.id)

    def generateOrderID():
        return str(random.randint(1000000000, 9999999999) * client.id * random.randint(3, 7))[:10]

    orderID = generateOrderID()

    while Order.objects.filter(order_id = orderID).exists():
        orderID = generateOrderID()

    for cart in Cart.objects.filter(client = client):
        Order.objects.create(order_id = orderID, product = cart.product, client = client)
        cart.delete()

    return redirect('client-orders')

def clientOrders(request):

    queryOrders = 'select p.name as productName, p.product_id as productID, p.price as productPrice, count(p.product_id) as productCount, p.image as productImage, o.order_id as orderID, o.product_id, o.client_id as clientID, sum(p.price) as sumForCount, p.id from Orders as o join Products as p on p.id = o.product_id where clientID = ' + str(request.user.id) + ' group by clientID, productID, orderID'
    orders = Order.objects.raw(queryOrders)
    # Нужные поля:
    # productID - код товара
    # productName - имя товара
    # productImage - изображение товара
    # productPrice - цена за единицу товара
    # productCount - количество единиц товара в заказе
    # sumForCount - цена за все единицы указанного товара
    # clientID - id клиента (индекс в таблице)
    # orderID - номер заказа (поле из таблицы Orders, не индекс таблицы)

    querySum = 'select o.id, o.client_id as clientID, o.order_id as orderID, sum(p.price) as totalSum from Products as p join Orders as o on o.product_id = p.id where clientID = ' + str(request.user.id) + ' group by orderID, clientID'
    sums = Order.objects.raw(querySum)
    # Нужные поля:
    # clientID - id клиента (индекс в таблице)
    # orderID - номер заказа (поле из таблицы Orders, не индекс таблицы)
    # totalSum - сумма за весь заказ

    print('\n\n\t\t\t---Заказы клиента: ', orders.query, '\n')
    print('\n\n\t\t\t---Cуммы заказов клиента: ', sums.query, '\n')

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/client-orders.html',
        {
            'orders': orders,
            'sums': sums,
            'orders': orders,
            'title':'Заказы',
            'year':datetime.now().year,
        }
    )