from django import forms
<<<<<<< HEAD

from accounts.validators import allow_only_images_validator
from .models import Category, FoodItem
=======
from .models import Category
>>>>>>> e8a54bb67064b1613458a1ab989ea24119096410


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
<<<<<<< HEAD
        fields = ['category_name', 'description']


class FoodItemForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}), validators=[allow_only_images_validator])
    class Meta:
        model = FoodItem
        fields = ['category', 'food_title', 'description', 'price', 'image', 'is_available']
=======
        fields = ['category_name', 'description']
>>>>>>> e8a54bb67064b1613458a1ab989ea24119096410
