

from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
# Authentication Views
from .views.login_views import admin_login,admin_logout

# Dashboard Views
from .views.dasboard_views import dashboard

# Category Views
from .views.category_views import admin_category_list,admin_category_add,category_edit,category_delete

#  SubCategory 
from .views.subcategory_views import ( 
    admin_subcategory_list,
    Admin_subcategory_add,
    admin_subcategory_edit,
    admin_subcategory_delete )

from .views.product_views import (
              admin_product_add,
              admin_product_list,
              admin_product_delete,
              admin_product_edit
              )

from .views.brands import(
               
                  admin_brand_list,
                   admin_brand_add,
                  admin_brand_delete,
                  admin_brand_edit
)

urlpatterns = [

    # ========================================
    # ADMIN LOGIN
    # ========================================

    path(
        'login/',
        admin_login,
        name='admin_login'
    ),

    path('logout/', admin_logout,name='admin_logout'),

    # ========================================
    # ADMIN DASHBOARD
    # ========================================

    path(
        'dashboard/',
        dashboard,
        name='dashboard'
    ),

    # ========================================
    # CATEGORY MANAGEMENT
    # ========================================

    path(
        'categories/',
        admin_category_list,
        name='admin_category_list'
    ),
     path(
        'categories/add/',
        admin_category_add,
        name='admin_category_add'
    ),
 path(
        'categories/edit/<int:id>/',
        category_edit,
        name='category_edit'
    ),

path(
        'categories/delete/<int:id>/',
        category_delete,
        name='category_delete'
    ),




# ========================================
 # SubCATEGORY MANAGEMENT
# ========================================

path(
        'subcategories/',
        admin_subcategory_list,
        name='admin_subcategory_list'
    ),

path('subcategories/add/',Admin_subcategory_add,name='admin_subcategory_add'),

path('subcategories/edit/<int:id>/',admin_subcategory_edit,name='admin_subcategory_edit'),

path('subcategories/delete/<int:id>/',admin_subcategory_delete,name='admin_subcategory_delete'),



# ========================================
# PRODUCTS  MANAGEMENT
# ========================================

path('product/',admin_product_list,name='admin_product_list'),
path('product/add',admin_product_add,name='admin_product_add'),
path('product/edit/<int:id>/',admin_product_edit,name='admin_product_edit'),
path('product/delete/<int:id>/',admin_product_delete,name='admin_product_delete'),

# =================================
# Brnads Routing 
# ==================================

path('brand/',admin_brand_list,name='admin_brand_list'),
path('brand/add',admin_brand_add,name='admin_brand_add'),
path('brand/edit/<int:id>/',admin_brand_edit,name='admin_brand_edit'),
path('brand/delete/<int:id>/',admin_brand_delete,name='admin_brand_delete'),


]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
