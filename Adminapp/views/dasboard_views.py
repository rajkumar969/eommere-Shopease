from django.shortcuts import render, redirect
from django.contrib import messages

from authentication.models import user


# ========================================
# ADMIN DASHBOARD
# ========================================

def dashboard(request):

    # =====================================
    # GET ADMIN SESSION
    # =====================================

    admin = request.session.get(
        'admin_id'
    )

    # =====================================
    # CHECK ADMIN LOGIN
    # =====================================

    if not admin:

        messages.error(
            request,
            'Please Login Admin First'
        )

        return redirect(
            'admin_login'
        )

    # =====================================
    # VERIFY ADMIN USER
    # =====================================

    try:

        admin_user = user.objects.get(
            id=admin,
            is_active=True,
            is_staff=True
        )

    except user.DoesNotExist:

        # Invalid session remove
        request.session.flush()

        messages.error(
            request,
            'Admin Session is Invalid'
        )

        return redirect(
            'admin_login'
        )

    # =====================================
    # SHOW DASHBOARD
    # =====================================

    return render(
        request,
        'Adminapp/dashboard.html',
        {
            'admin_user': admin_user
        }
    )