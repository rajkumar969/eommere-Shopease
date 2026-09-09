from django.shortcuts import render,redirect
from django.contrib import messages
from .models import user
from django.contrib.auth.hashers import make_password,check_password


def register(request):
    if request.method=='POST':
        name=request.POST.get('fullname')
        email=request.POST.get("email")
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        hash_pass=make_password(password)
        #---------------------------------------------
        # validation 
        # --------------------------------------------,
         
        if user.objects.filter(email=email).exists():
                messages.error(request,'Email Aready Registered')
                return redirect('register')
            
        if user.objects.filter(phone=phone).exists():
               messages.error(request,'Phone already register')
               return redirect('register')
        
        #---------------------------------------
        # create  customer on database
        #----------------------------------------------
        
        customer=user.objects.create(
        username=name,
        email=email,
        password=hash_pass,
        phone=phone
        

        )
        customer.save()
        messages.success(request,'Registration Successfuly')
        return redirect('login')
    return render(request,'register.html',{'custormer':customer})


def login(request):
    if request.method=="POST":
         email=request.POST.get('email')
         password=request.POST.get('password')
         try:
              user_obj=user.objects.get(email=email)
              if check_password(password,user_obj.password):
                   
                #    Create session
                   request.session['userid']=user_obj.id

                # store  username  in session   
                   request.session['username']=user_obj.username

                 # Session save

                   print("Session Set:", request.session.get("userid"))
                   
                   messages.success(request,'Login Successful')

                #  go to the  main page  
                   return redirect('home')

              else: 
                   messages.warning(request,'Wrong Password')  
         except user.DoesNotExist :
              messages.warning(request,'User Not Found') 
              return redirect('register')          
    return render(request,'login.html')


def home(request):
    return render(request,'home.html')

def logout(request):
     request.session.flush()
     return render(request,'login.html')


# Create your views here.
