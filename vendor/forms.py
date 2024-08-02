from django import forms
from .models import Vendor
<<<<<<< HEAD
from accounts.validators import allow_only_images_validator
=======
from accounts.validdators import allow_only_images_validator
>>>>>>> e8a54bb67064b1613458a1ab989ea24119096410
class VendorForm(forms.ModelForm):
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}), validators=[allow_only_images_validator])

    class Meta:
        model=Vendor
        fields=['vendor_name', 'vendor_license']