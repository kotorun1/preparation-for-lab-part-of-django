from django.urls import path
from .views import register, logout, auth, listProductsView, createProductView, detailProductView, createCartView, \
    getCartView, orderView, patchCartView

urlpatterns = [
    path('signup', register),
    path('login', auth),
    path('logout', logout),
    path('products', listProductsView),
    path('product', createProductView),
    path('product/<int:id>', detailProductView),
    path('cart', getCartView),
    path('cart', patchCartView),
    path('cart/<int:product_id>', createCartView),
    path('order', orderView)
]
