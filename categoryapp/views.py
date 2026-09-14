from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from authentication.models import user
from .models import Category, Products, Brand, Subcategory


# =========================
# HOME PAGE
# =========================

def home(request):

    products = Products.objects.filter(
        status=True
    ).order_by('-id')[:8]

    categories = Category.objects.filter(
        status=True
    )[:6]

    context = {
        'products': products,
        'categories': categories,
    }

    return render(
        request,
        'home.html',
        context
    )


# =========================
# CATEGORY PAGE
# =========================

def category(request):

    categories = Category.objects.filter(
        status=True
    )

    return render(
        request,
        "category.html",
        {
            "categories": categories
        }
    )


# =========================
# PRODUCT LIST PAGE
# =========================

def products_list(request):

    products = Products.objects.filter(
        status=True
    )

    categories = Category.objects.filter(
        status=True
    )

    context = {
        'products': products,
        'categories': categories
    }

    return render(
        request,
        'products_list.html',
        context
    )


# =========================
# PRODUCT DETAIL
# =========================

def product_detail(request, product_id):

    product = get_object_or_404(
        Products,
        id=product_id,
        status=True
    )

    related_products = Products.objects.filter(
        category=product.category,
        status=True
    ).exclude(
        id=product.id
    )[:4]

    context = {
        'product': product,
        'related_products': related_products
    }

    return render(
        request,
        'products/product_details.html',
        context
    )


# =========================
# CART
# =========================

def cart(request):
    return render(request, 'cart.html')


# =========================
# WISHLIST
# =========================

def wishlist(request):
    return render(request, 'wishlist.html')


# =========================
# PROFILE
# =========================

def profile(request):

    user_id = request.session.get('userid')

    if not user_id:

        messages.error(
            request,
            'Please login first'
        )

        return redirect('login')

    try:

        user_obj = user.objects.get(
            id=user_id
        )

    except user.DoesNotExist:

        messages.warning(
            request,
            "User Account not Found"
        )

        return redirect('login')

    return render(
        request,
        'profile.html',
        {
            'user': user_obj
        }
    )


# =========================
# ORDERS
# =========================

def orders(request):

    return render(
        request,
        'orders.html'
    )