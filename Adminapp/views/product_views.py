from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.utils.text import slugify

from categoryapp.models import (
     Products, 
     Category,
    Subcategory,
    Brand ,)


    # =====================================
    # CHECK ADMIN LOGIN
    # =====================================


def  login_required(request):
      if not request.session.get(
            'admin_id'
        ):
    
            messages.error(
                request,
                'Please Admin Login First'
            )
    
            return False
      return True


def admin_product_list(request):
       if not login_required(request):
            return redirect('admin_login')
       products = Products.objects.select_related(  'category',
        'subcategory',
        'brand').all()
       context = {'products': products}
       return render( request,'Adminapp/products/admin_product_list.html',  context)
    


def admin_product_add(request):

    #  First of all Admin login Required for  any CRUD operation .

    if not login_required(request):
         return redirect('admin_login')

    # =====================================
    # GET DATA FOR FORM
    # =====================================

    categories = Category.objects.filter(status=True)

    subcategories = Subcategory.objects.filter(status=True)

    brands = Brand.objects.filter(status=True)


    
    # Fetch data  from Add product Form 

    if request.method=='POST':
         category_id=request.POST.get('category')
         subcategory_id=request.POST.get('subcategory')
         brand_id=request.POST.get('brand')
         name=request.POST.get('product_name','').strip()
         slug=request.POST.get('slug','').strip()
         price=request.POST.get('price')
         discount=request.POST.get('discount')
         stock=request.POST.get('stock')
         rating=request.POST.get('rating')
         image=request.FILES.get('image')
         description=request.POST.get('description','').strip()
         
         status = True if request.POST.get(
            'status'
        ) else False
         
        # =====================================
        # BASIC VALIDATION
        # =====================================

         if not category_id:
            messages.error( request, 'Please select a category.')
            return redirect('admin_product_add')


         if not subcategory_id:
            messages.error( request,'Please select a subcategory.')
            return redirect('admin_product_add')


         if not brand_id:
            messages.error( request,'Please select a brand.')
            return redirect('admin_product_add')


         if not name:
            messages.error( request,'Product name is required.')
            return redirect('admin_product_add')

         if not price:
            messages.error( request,'Product price is required.')
            return redirect('admin_product_add')


         if not image:
            messages.error(request,'Product image is required.')
            return redirect('admin_product_add')

         status = True if request.POST.get('status' ) else False

         # =====================================
        # GET DATABASE OBJECTS
        # =====================================
         category=get_object_or_404(Category,id=category_id,status=True)
         subcategory=get_object_or_404(Subcategory,id=subcategory_id,status=True)
         brand=get_object_or_404(Brand,id=brand_id,status=True)

        # =====================================
        # IMPORTANT VALIDATION
        #
        # Check selected subcategory belongs
        # to selected category
        # =====================================
         if subcategory.category_name_id !=category.id:
             messages.error(request,'Select Subcategory  is  not belongs  to this Category')
             return redirect('admin_product_add')
         if Products.objects.filter(
              product_name__iexact=name
         ).exists():
             messages.error(request,'Product Already Exsist')
             return redirect('admin_product_add')

         # =====================================
        # CHECK DUPLICATE SLUG
        # =====================================

         if Products.objects.filter(
            slug=slug
        ).exists():

            messages.error(
                request,
                'Slug already exists.'
            )

            return redirect('admin_product_add')
             
         
# data save in Database

         Products.objects.create(
                category=category,
                subcategory=subcategory,
                brand=brand,
                product_name=name,
                slug=slug,
                price=price,
                discount=discount if discount else None,
                description=description,
                stock=stock,
                image=image,
                 rating=rating if rating else 0,
                status=status 
            ) 
         # =====================================
    # GET REQUEST
    # =====================================

        #  context = {

        # 'categories': categories,

        # 'subcategories': subcategories,

        # 'brands': brands

        # }
         messages.success(request,'Products Scussessfully added')

         return redirect('admin_product_list')  
    return render(request,'Adminapp/products/admin_product_add.html',{ 'categories': categories,
    
            'subcategories': subcategories,
    
            'brands': brands
    } )
        
        
         


    


def admin_product_edit(request, id):

    # =====================================
    # ADMIN LOGIN CHECK
    # =====================================

    if not login_required(request):
        return redirect('admin_login')

    # =====================================
    # GET PRODUCT
    # =====================================

    product = get_object_or_404(  Products,id=id )

    # =====================================
    # FETCH FORM DATA
    # =====================================

    categories = Category.objects.filter(status=True)
    subcategories = Subcategory.objects.filter( status=True)
    brands = Brand.objects.filter( status=True)

    # =====================================
    # POST REQUEST
    # =====================================

    if request.method == 'POST':
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')
        brand_id = request.POST.get('brand')
        name = request.POST.get( 'product_name','').strip()
        slug = request.POST.get('slug','').strip()
        price = request.POST.get('price')
        discount = request.POST.get('discount')
        stock = request.POST.get('stock')
        rating = request.POST.get('rating')
        image = request.FILES.get('image')
        description = request.POST.get('description',  '').strip()
        status = True if request.POST.get(  'status' ) else False


        # =====================================
        # VALIDATION
        # =====================================

        if not category_id:
            messages.error(request, 'Please select a category.')
            return redirect( 'admin_product_edit',id=product.id )

        if not subcategory_id:
            messages.error( request, 'Please select a subcategory.' )
            return redirect('admin_product_edit',id=product.id)


        if not brand_id:
            messages.error( request, 'Please select a brand.')
            return redirect( 'admin_product_edit',  id=product.id)


        if not name:

            messages.error(  request, 'Product name is required.' )

            return redirect(
                'admin_product_edit',
                id=product.id
            )


        if not price:

            messages.error(
                request,
                'Price is required.'
            )

            return redirect(
                'admin_product_edit',
                id=product.id
            )


        # =====================================
        # GET FOREIGN KEY OBJECTS
        # =====================================

        category = get_object_or_404( Category, id=category_id)
        subcategory = get_object_or_404(Subcategory,id=subcategory_id )
        brand = get_object_or_404( Brand, id=brand_id)


        # =====================================
        # CHECK SUBCATEGORY BELONGS TO CATEGORY
        # =====================================

        if subcategory.category_name_id != category.id:
            messages.error( request, 'Selected subcategory does not belong to this category.')
            return redirect ('admin_product_edit',  id=product.id )


        # =====================================
        # GENERATE SLUG
        # =====================================

        if not slug:
            slug = slugify(name)


        # =====================================
        # CHECK DUPLICATE PRODUCT NAME
        # EXCLUDE CURRENT PRODUCT
        # =====================================

        if Products.objects.exclude(id=product.id).filter( product_name__iexact=name).exists():
            messages.error( request, 'Another product with this name already exists.')
            return redirect('admin_product_edit', id=product.id)


        # =====================================
        # CHECK DUPLICATE SLUG
        # EXCLUDE CURRENT PRODUCT
        # =====================================

        if Products.objects.exclude( id=product.id).filter(  slug=slug).exists():
            messages.error(request,'Another product with this slug already exists.')
            return redirect( 'admin_product_edit', id=product.id)
            


        # =====================================
        # UPDATE PRODUCT
        # =====================================

        product.category = category
        product.subcategory = subcategory
        product.brand = brand
        product.product_name = name
        product.slug = slug
        product.price = price
        product.discount = discount if discount else None
        product.stock = stock
        product.rating = rating if rating else 0
        product.description = description
        product.status = status


        # UPDATE IMAGE ONLY IF NEW IMAGE EXISTS

        if image:
            product.image = image
        product.save()

        messages.success( request, 'Product successfully updated.')
        return redirect('admin_product_list')
        


    # =====================================
    # GET REQUEST
    # =====================================

    context = {

        'product': product,

        'categories': categories,

        'subcategories': subcategories,

        'brands': brands

    }


    return render(
        request,
        'Adminapp/products/admin_product_edit.html',
        context
    )
             
                      
    




def admin_product_delete(request, id):
    if not  login_required(request):
        return redirect('admin_login')
    product=get_object_or_404(
        Products,
        id=id
    )
    product.delete()
    messages.success(request,'Deleted product successfully')
    return redirect('admin_product_list')