from django.urls import path
from .import views 
urlpatterns = [
    
   path("category/", views.category, name="category"),
   path('products/',views.products_list,name='products_list'),
   path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/',views.cart,name='cart'),
    path('wishlist/',views.wishlist,name="wishlist"),
    path('profile/',views.profile,name='profile'),
    path('orders/',views.orders,name='orders')
    
]