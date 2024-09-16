from vendor.models import Vendor
from django.conf import settings
from marketplace.models import Cart, FoodItem

def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)

def get_google_api(request):
    return{'GOOGLE_API_KEY':settings.GOOGLE_API_KEY}


def get_cart_amounts(request):
    subtotal = 0
    tax = 0
    grand_total = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user = request.user)
        for item in cart_items:
            fooditem = FoodItem.objects.get(pk=item.fooditem.id)
            subtotal += (fooditem.price * item.quantity)

        grand_total = subtotal + tax
    return dict(subtotal=subtotal, tax=tax, grand_total = grand_total)