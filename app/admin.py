from django.contrib import admin
from .models import Product, Client, Сategories, Album, Images, News, Comment, Status, Order, Cart

class ProductAdmin(admin.ModelAdmin):
  list_display = ['name', 'product_id', 'price', 'album', 'category']

class ClientAdmin(admin.ModelAdmin):
  list_display = ['username', 'first_name', 'last_name', 'email', 'phone']

class СategoriesAdmin(admin.ModelAdmin):
  list_display = ['name']

class AlbumAdmin(admin.ModelAdmin):
  list_display = ['name']

class ImagesAdmin(admin.ModelAdmin):
  list_display = ['album', 'img']

class NewsAdmin(admin.ModelAdmin):
  list_display = ['title', 'date']

class CommentAdmin(admin.ModelAdmin):
  list_display = ['author', 'product', 'date']

class StatusAdmin(admin.ModelAdmin):
  list_display = ['text', 'colorHEX']

class OrderAdmin(admin.ModelAdmin):
  list_display = ['order_id', 'product', 'client', 'status', 'date']

class CartAdmin(admin.ModelAdmin):
  list_display = ['product', 'client']

admin.site.register(Product, ProductAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Сategories, СategoriesAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)