from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .forms import VendorForm
from .models import Vendor
from accounts.forms import UserProfileForm
from accounts.models import UserProfile

# Create your views here.
def profile(request):
    profile = get_object_or_404(UserProfile, user= request.user)
    vendor = get_object_or_404(Vendor, user = request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)

        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "Settings Updated.")
            return redirect('profile')
        
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
        
    else:
        
        profile_form=UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)

    context ={
        'profile_form':profile_form,
        'vendor_form':vendor_form,
        'profile':profile,
        'vendor':vendor,
    }
    return render(request, 'accounts/vendor/profile.html', context)