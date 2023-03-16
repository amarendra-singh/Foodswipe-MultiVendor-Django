from django.shortcuts import render, redirect
from django.contrib import messages
from . forms import UserForm
from . models import User
# Create your views here.
def registerUser(request):
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
            phone_number=form.cleaned_data['phone_number']
            password=form.cleaned_data['password']

            user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,phone_number=phone_number,password=password)
            user.role=User.CUSTOMER
            user.save()
            messages.success(request, "Your account has been registered succesfully")

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