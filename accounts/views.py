from django.shortcuts import render, redirect
from django.contrib import messages,auth
from .utils import detectUser
from vendor.forms import VendorForm
from . forms import UserForm
from . models import User,UserProfile
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied


# Create your views here.

def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def home(request):
    return render(request,'home.html')

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('dashboard') 
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # user = form.save(commit=False)
            # user.role = User.CUSTOMER
            # user.save()

            username = form.cleaned_data['username']
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            # phone_number=form.cleaned_data['phone_number']
            password=form.cleaned_data['password']

            user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
            user.role=User.CUSTOMER
            user.save()
            messages.success(request, 'Your account has been registered sucessfully!')

            return redirect('registerUser')
        else:
            print("Invalid Form")
            print(form.errors)
    else:
        form = UserForm
    context = {
        'form':form,
    }
    return render(request, 'accounts/registerUser.html', context)

def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('dashboard') 
    if request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)

        if form.is_valid() and v_form.is_valid:
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()

            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, "Your account has been registered successfully")
            return redirect('registerVendor')
        else:
            print('Invaild form')
            print(form.errors)
    else:
        form=UserForm()
        v_form=VendorForm()

    context={
        'form': form,
        'v_form': v_form,
    }
    return render(request, 'accounts/registerVendor.html', context)

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('myaccount') 

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            auth.login(request,user)
            messages.success(request,"Logged in successfully")
            return redirect('myaccount')
        else:
            messages.error(request,"Invalid Email Address or Password")
            return redirect('login')

    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,"You are logged out")
    return redirect('login')

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):
    return render(request, 'accounts/customerDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')

@login_required(login_url='login')
def myaccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)