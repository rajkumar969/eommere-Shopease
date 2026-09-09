from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.utils.text import slugify

from categoryapp.models import Category


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

# ========================================
# CATEGORY LIST
# ========================================

def admin_category_list(request):

   if not login_required(request):
       return redirect('admin_login')
  
    # =====================================
    # GET ALL CATEGORIES
    # =====================================

   categories = Category.objects.all()

  
   print("Count:", categories.count())

    # =====================================
    # CONTEXT
    # =====================================

   context = {
        'categories': categories
    }

    # =====================================
    # RENDER CATEGORY PAGE
    # =====================================

   return render(
        request,
        'Adminapp/admin_category_list.html',
        context
    )

# =========================================================
# 1. CATEGORY Add
# =========================================================

def admin_category_add(request):
     if not login_required(request):
          return redirect('admin_login')
     if request.method=="POST":
          category_name=request.POST.get('category_name','').strip()
          description=request.POST.get('description','').strip()
          image=request.FILES.get('profile_image')
          status=request.POST.get('status')
          slug=request.POST.get('slug','').strip()

          print("Category Name:", category_name)
          print("Slug:", slug)
        #======================================
        # Validation 
        # =======================================   

          if not category_name:
              messages.error(request,'category Name required ')

              return redirect('admin_category_add')
          
          if  not  slug:
               slug=slugify(category_name)

            #=================================
            # Check Dublicate Category name .
            # ==================================

          if Category.objects.filter(category_name=category_name ).exists():   
                messages.error(request,"category All ready Exist.") 
                return redirect('admin_category_add')
          
             #=================================
            # Check Dublicate Category name .
            # ==================================

          if Category.objects.filter(slug=slug).exists():
              messages.error(request,' This  is slug  Already Exists')
              return redirect('admin_category_add')
         
          print("CATEGORY NAME:", repr(category_name))
          print("SLUG:", repr(slug)) 
        # =========================================
        # CREATE CATEGORY
        # =========================================
          Category.objects.create(
               category_name=category_name,
               description=description,
               profile_image=image,
                slug=slug, 
               status=True if status else False

          ) 
          messages.success(request,'Category Successfully Added.')

          return redirect('admin_category_list')
       # =====================================
    # GET REQUEST
    # =====================================
     return render(
             request,
            'Adminapp/category_add.html'
    )


    # =====================================
    # Category Edit
    # =====================================
        
def category_edit(request,id):
    if not  login_required(request):
         return redirect('admin_login')
    category=get_object_or_404(
         Category,
         id=id
    ) 
    if request.method=="POST":
         category_name=request.POST.get('category_name')
         slug=request.POST.get('slug')
         description=request.POST.get('description')
         status=request.POST.get('status')
         image=request.FILES.get('profile_image')

         category.category_name=category_name
         category.slug=slug 
         category.description=description
         category.status = True if request.POST.get('status') else False
         category.profile_image=image

         if image:
           category.profile_image=image
         category.save()
         messages.success(request,'Updated is successfully')

         return redirect('admin_category_list')

        
    return render(request,'Adminapp/category_edit.html',{'category':category})

     

# =====================================
    # Category DELETE
    # =====================================
        
def category_delete(request,id):
    if not  login_required(request):
         return redirect('admin_login')
    category=get_object_or_404(Category,id=id)
    category.delete()
    messages.success(request,'Successfully Deleted Category')
         
    
    return redirect('admin_category_list')

     

