from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.utils.text import slugify

from categoryapp.models import Category, Subcategory,Products,Brand
from .category_views import login_required


def admin_brand_list(request):
    if  not login_required(request):
        return redirect('admin_login')
    brands=Brand.objects.all().order_by('-created_at')
    context={
        'brands': brands
    }
    return render(request,'Adminapp/Brands/admin_brand_list.html',context)


def admin_brand_add(request):
    if  not login_required(request):
        return redirect('admin_login')
    
    # get data from  add form 

    if request.method=="POST":
        b_name=request.POST.get('name','').strip()
        b_slug=request.POST.get('slug','').strip()
        b_image=request.FILES.get('image')
        b_description=request.POST.get('description','').strip()
        b_status= True if request.POST.get('status') else False 

        # Some  validation  
        if not b_name:
            messages.error(request,'Brand name Required')
            return redirect('admin_brand_add')
        if  not b_slug:
            b_slug=slugify(b_name)
        
        # Check dubplicate name  and  slug  or  not
        if  Brand.objects.filter( name__iexact=b_name).exists():
                messages.error(request,'Brand Name Already Exists')
                return redirect('admin_brand_add')
        
        if Brand.objects.filter(slug=b_slug).exists():
            messages.error(request,'Brand Name Already Exists')
            return redirect('admin_brand_add')

        # Create  Brands
        Brand.objects.create(
            name=b_name,
            slug=b_slug,
            image=b_image,
            description=b_description,
            status=b_status
        )
        messages.success(request,'Successfully added Brands ')
        
        return  redirect('admin_brand_list')
    return render(request,'Adminapp/Brands/admin_brand_add.html')

    
    




def admin_brand_edit(request):

    pass
def admin_brand_delete(request):
    pass