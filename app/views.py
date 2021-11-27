"""
Definition of views.
"""

from typing import Any
from django.contrib.auth.models import User
from django.db.models import query
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

import types

from django.db.models import Value

from django.contrib.auth.forms import UserCreationForm

from app.forms import CommentForm

from .models import Cart, Comment, Images, Order, Product, Status, Сategories

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

    q = '''
    select
    p.id,
    p.name as productName,
    p.product_id as productCode,
    p.description as productDescription,
    p.price as productPrice
    from Products as p
    '''

    products_tmp = Product.objects.raw(q)

    # products_tmp = Product.objects.all()

    class Product_tmp:
        def __init__(self, product, images):
            self.productID = product.id
            self.productCode = product.productCode
            self.productName = product.productName
            self.productDescription = product.productDescription
            self.productPrice = product.productPrice
            self.productImages = []
            for img in images:
                self.productImages.append(str(img.img.url))
            self.productImage = self.productImages[0]

    products = []

    for product in products_tmp:
        images = Images.objects.filter(album_id = product.album_id)
        products.append(Product_tmp(product, images))

    categories = Сategories.objects.all()

    print('\n\n\t\t\t--- Каталог:\n' + str(products) + '\n')

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/catalog.html',
        {
            'title': 'Товары',
            'categories': categories,
            'products': products,
            # 'images': images,
            'year':datetime.now().year,
            }
        )

def catergory(request, parametr):
    query = '''select * from Products as p 
    join Сategories as c on p.category_id = c.id
    where c.id = 
    ''' + str(parametr)

    products = Product.objects.raw(query)
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

    querySum = '''select 
    o.id, o.client_id as clientID, o.order_id as orderID,
    sum(p.price) as totalSum,
    s.text as orderStatus, s.colorHEX as statusColor
    from Products as p
    join Orders as o
    on o.product_id = p.id
    join Statuses as s
    on o.status_id = s.id 
    group by o.order_id 
    order by s.id, o.date'''

    queryOrders = '''select
    o.client_id as clientID, o.order_id as orderID,
    p.id, p.product_id as productID, p.name as productName,
    p.price as productPrice, count(p.id) as productCount, sum(p.price) as sumForCount
    from Orders as o
    join Products as p
    on o.product_id = p.id
    group by p.id, o.order_id'''

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

    queryCart = '''select
    c.id, c.product_id,
    p.name as productName, p.price as productPrice, p.image as productImage,
    p.product_id as productID, sum(p.price) as sumForCount, count(p.id) as productCount
    from Carts as c
    join Products as p
    on p.id = c.product_id
    where c.client_id = 
    ''' + str(request.user.id) + ' group by productID'

    carts = Cart.objects.raw(queryCart)

    # print('\n\n\t\t\t---Клиент: ', client.query, '\n')
    # print('\n\n\t\t\t---Корзина: ', carts.query, '\n')

    totalSum = 0
    for cart in carts:
        totalSum += cart.product.price * cart.productCount

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

    queryOrders = '''select 
    p.name as productName, p.product_id as productID, p.price as productPrice,
    count(p.product_id) as productCount, p.image as productImage,
    o.order_id as orderID, o.product_id, o.client_id as clientID,
    sum(p.price) as sumForCount, p.id 
    from Orders as o 
    join Products as p
    on p.id = o.product_id
    where clientID = ''' + str(request.user.id) + '''
    group by clientID, productID, orderID'''
    
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

    querySum = '''select
    o.id, o.client_id as clientID, o.order_id as orderID,
    sum(p.price) as totalSum,
    s.text as orderStatus, s.colorHEX as statusColor
    from Products as p
    join Orders as o
    on o.product_id = p.id
    join Statuses as s
    on o.status_id = s.id
    where clientID = ''' + str(request.user.id) + '''
    group by orderID, clientID
    order by o.date'''

    sums = Order.objects.raw(querySum)
    # Нужные поля:
    # clientID - id клиента (индекс в таблице)
    # orderID - номер заказа (поле из таблицы Orders, не индекс таблицы)
    # totalSum - сумма за весь заказ
    # orderStatus - статус заказа
    # statusColor - цвет статуса

    # print('\n\n\t\t\t---Заказы клиента: ', orders.query, '\n')
    # print('\n\n\t\t\t---Cуммы заказов клиента: ', sums.query, '\n')

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

def approveOrder(request, parametr):

    orders = Order.objects.filter(order_id = parametr)
    status = Status.objects.get(text = 'Подтвержден')

    for order in orders:
        order.status = status
        order.save()

    return redirect('manager-orders')

def rejectOrder(request, parametr):
    orders = Order.objects.filter(order_id = parametr)
    status = Status.objects.get(text = 'Отклонен')

    for order in orders:
        order.status = status
        order.save()

    return redirect('manager-orders')

def resetOrder(request, parametr):
    orders = Order.objects.filter(order_id = parametr)
    status = Status.objects.get(text = 'В обработке')

    for order in orders:
        order.status = status
        order.save()

    return redirect('manager-orders')

def deleteOrder(request, parametr):
    orders = Order.objects.filter(order_id = parametr)

    for order in orders:
        order.delete()

    return redirect('manager-orders')

def imgs(request):
    query = 'select * from Images'

    images = Images.objects.raw(query)

    print("\n\n\t\t\t---Картинки:\n\n" + str(images.query) + "\n\n")

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/imgs.html',
        {
            'images': images,
            'year':datetime.now().year,
            }
        )