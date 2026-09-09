from django.shortcuts import render, redirect
from authentication.models import user
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages


# ========================================
# MAKE ADMIN FUNCTION
# ========================================

def make_admin(username, email, phone, password):

    try:
        # Check user already exists
        user_admin = user.objects.get(
            username=username
        )

        # Existing user ko update karo
        user_admin.email = email
        user_admin.phone = phone
        user_admin.password = make_password(password)

        user_admin.is_active = True
        user_admin.is_staff = True
        user_admin.is_superuser = True

        user_admin.save()

        print(
            f"{username} is now Admin/Superuser"
        )

    except user.DoesNotExist:

        # User nahi mila to new user create karo
        user_admin = user.objects.create(
            username=username,
            email=email,
            phone=phone,
            password=make_password(password),
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )

        print(
            f"{username} Admin/Superuser created successfully"
        )

    return user_admin


# ========================================
# ADMIN LOGIN
# ========================================

def admin_login(request):

    # ========================================
    # ALREADY LOGGED IN
    # ========================================

    if request.session.get('admin_id'):
        return redirect('dashboard')

    # ========================================
    # LOGIN FORM SUBMISSION
    # ========================================

    if request.method == "POST":

        email = request.POST.get(
            'email',
            ''
        ).strip()

        passw = request.POST.get(
            'password',
            ''
        )

        # =====================================
        # BASIC VALIDATION
        # =====================================

        if not passw or not email:

            messages.error(
                request,
                'Please enter email and password'
            )

            return render(
                request,
                'Adminapp/admin_login.html'
            )

        # =====================================
        # FIND USER
        # =====================================

        try:

            user_object = user.objects.get(
                email=email
            )

        except user.DoesNotExist:

            messages.error(
                request,
                "Invalid Email and Password"
            )

            return render(
                request,
                'Adminapp/admin_login.html'
            )

        # =====================================
        # CHECK ACTIVE STATUS
        # =====================================

        if not user_object.is_active:

            messages.error(
                request,
                'Your account is inactive'
            )

            return render(
                request,
                'Adminapp/admin_login.html'
            )

        # =====================================
        # CHECK ADMIN / STAFF STATUS
        # =====================================

        if not user_object.is_staff:

            messages.error(
                request,
                'You are not authorized to access Admin Panel.'
            )

            return render(
                request,
                'Adminapp/admin_login.html'
            )

        # =====================================
        # CHECK PASSWORD
        # =====================================

        if not check_password(
            passw,
            user_object.password
        ):

            messages.error(
                request,
                'Invalid Email and Password'
            )

            return render(
                request,
                'Adminapp/admin_login.html'
            )

        # =====================================
        # CREATE ADMIN SESSION
        # =====================================

        request.session['admin_id'] = user_object.id

        request.session['admin_username'] = (
            user_object.username
        )

        request.session['admin_email'] = (
            user_object.email
        )

        request.session.save()

        messages.success(
            request,
            "Admin Login Successful"
        )

        return redirect('dashboard')

    # =====================================
    # SHOW LOGIN PAGE
    # =====================================

    return render(
        request,
        'Adminapp/admin_login.html'
    )
# =============================================================================
# Admin Logout dashboard
# =============================================================================
def admin_logout(request):
    #  Admin logout 
    request.session.flush()
    messages.success(request,'Admin Log out successfully ')
    return redirect('admin_login')