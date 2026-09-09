from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.utils.text import slugify

from categoryapp.models import Category, Subcategory


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


def admin_subcategory_list(request):

    if not login_required(request):
        return redirect('admin_login')

    subcategories = Subcategory.objects.select_related(
        'category_name'
    ).all()

    context = {
        'subcategories': subcategories
    }

    return render(
        request,
        'Adminapp/subcategory/admin_subcategory_list.html',
        context
    )

             
def Admin_subcategory_add(request):

    # =====================================
    # CHECK ADMIN LOGIN
    # =====================================

    if not login_required(request):
        return redirect('admin_login')


    # =====================================
    # GET ACTIVE CATEGORIES
    # =====================================

    categories = Category.objects.filter(status=True)


    # =====================================
    # FORM SUBMISSION
    # =====================================

    if request.method == "POST":

        category_id = request.POST.get('category')
        name = request.POST.get('name', '').strip()
        slug = request.POST.get('slug', '').strip()
        description = request.POST.get('description', '').strip()

        status = request.POST.get('status')


        # =====================================
        # BASIC VALIDATION
        # =====================================

        if not category_id:

            messages.error(
                request,
                'Please select a category.'
            )

            return redirect('admin_subcategory_add')


        if not name:

            messages.error(
                request,
                'Subcategory name is required.'
            )

            return redirect('admin_subcategory_add')


        # =====================================
        # GET CATEGORY
        # =====================================

        category = get_object_or_404(
            Category,
            id=category_id,
            status=True
        )


        # =====================================
        # GENERATE SLUG
        # =====================================

        if not slug:

            slug = slugify(name)


        # =====================================
        # CHECK DUPLICATE SLUG
        # =====================================

        if Subcategory.objects.filter(
            slug=slug
        ).exists():

            messages.error(
                request,
                'This slug already exists.'
            )

            return redirect('admin_subcategory_add')


        # =====================================
        # CHECK DUPLICATE NAME
        # SAME CATEGORY
        # =====================================

        if Subcategory.objects.filter(
            category_name=category,
            name__iexact=name
        ).exists():

            messages.error(
                request,
                'This subcategory already exists in this category.'
            )

            return redirect('admin_subcategory_add')


        # =====================================
        # CREATE SUBCATEGORY
        # =====================================

        Subcategory.objects.create(

            category_name=category,

            name=name,

            slug=slug,

            description=description,

            status=True if status else False

        )


        # =====================================
        # SUCCESS MESSAGE
        # =====================================

        messages.success(
            request,
            'Subcategory successfully added.'
        )


        return redirect(
            'admin_subcategory_list'
        )


    # =====================================
    # GET REQUEST
    # =====================================

    return render(
        request,
        'Adminapp/subcategory/admin_subcategory_add.html',
        {
            'categories': categories
        }
    )

# ===========================================
# Admin_Subcategory_edits 
# ============================================
def admin_subcategory_edit(request,id):
    if not login_required(request):
        return redirect('admin_login')
    subcategory=get_object_or_404(
        Subcategory,
        id=id
    )
    categories=Category.objects.filter(status=True)

    if request.method=='POST':
        category_id = request.POST.get('category')
        name = request.POST.get('name', '').strip()
        slug = request.POST.get('slug', '').strip()
        description = request.POST.get('description', '').strip()

        status = request.POST.get('status')

        if  not category_id:
            messages.error(request,'Please select Category ')
            return redirect('admin_subcategory_list',id=id)
        
        if not name:
            messages.error(request,'Subcategory Field Required ') 
            return redirect('admin_subcategory_list',id=id)
        
        category = get_object_or_404(
            Category,
            id=category_id,
            status=True
        )

        # =====================================
        # AUTO SLUG
        # =====================================

        if not slug:
            slug = slugify(name)

        # =====================================
        # DUPLICATE SLUG
        # EXCLUDE CURRENT SUBCATEGORY
        # =====================================

        if Subcategory.objects.filter(
            slug=slug
        ).exclude(
            id=id
        ).exists():

            messages.error(
                request,
                'This slug already exists.'
            )

            return redirect(
                'admin_subcategory_edit',
                id=id
            )

        # =====================================
        # DUPLICATE NAME
        # =====================================

        if Subcategory.objects.filter(
            category_name=category,
            name__iexact=name
        ).exclude(
            id=id
        ).exists():

            messages.error(
                request,
                'This subcategory already exists in this category.'
            )

            return redirect(
                'admin_subcategory_edit',
                id=id
            )

        # =====================================
        # UPDATE
        # =====================================

        subcategory.category_name = category
        subcategory.name = name
        subcategory.slug = slug
        subcategory.description = description
        subcategory.status = True if status else False

        subcategory.save()

        messages.success(
            request,
            'Subcategory successfully updated.'
        )

        return redirect('admin_subcategory_list')

    return render(
        request,
        'Adminapp/subcategory/admin_subcategory_edit.html',
        {
            'subcategory': subcategory,
            'categories': categories
        }
    )
# ==============================================
# Delete subcategory 
# ============================================

def admin_subcategory_delete(request,id):

    if not login_required(request):
        return redirect('admin_login')
    subcategory=get_object_or_404(
        Subcategory,
        id=id

    )
    subcategory.delete()
    messages.success(request, 'Subcategory Deleted Successfully')
    return redirect('admin_subcategory_list')
    
     
    
 