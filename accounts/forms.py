from django import forms
from . models import User, UserProfile
<<<<<<< HEAD
from .validators import allow_only_images_validator
=======
from .validdators import allow_only_images_validator
>>>>>>> e8a54bb67064b1613458a1ab989ea24119096410

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password']

    def clean(self):
        cleaned_data=super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password does not match")


class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs = {'placeholder': ' Enter you address', 'required':'required'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}), validators=[allow_only_images_validator])
    cover_picture = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}), validators=[allow_only_images_validator])

    # latitude = forms.
    class Meta:
        model = UserProfile
        fields = ['profile_picture','cover_picture','address','country','state','city','pin_code','latitude','longitude',]