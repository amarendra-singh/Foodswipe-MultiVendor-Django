from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from vendor.models import Vendor, OpeningHour
from menu.models import Category, FoodItem
from django.db.models import Prefetch,Q
from marketplace.models import Cart

from datetime import date, datetime
from marketplace.context_processors import get_cart_counter
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D 
from django.contrib.gis.db.models.functions import Distance

# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors':vendors,
        'vendor_count':vendor_count
    }
    return render(request, 'marketplace/listing.html', context)

def vendor_detail(request,vendor_slug):
    vendor= get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )
    
    opening_hour = OpeningHour.objects.filter(vendor=vendor).order_by('day','-from_hour')
    today_date = date.today()
    today = today_date.isoweekday()
    current_opening_hours = OpeningHour.objects.filter(vendor=vendor, day=today)


    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None

    context = {
        'vendor':vendor,
        'categories':categories,
        'cart_items':cart_items,
        'opening_hour':opening_hour,
        'current_opening_hours':current_opening_hours,
    }
    return render(request,'marketplace/vendor_detail.html', context)


def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with')== 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    check_cart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    check_cart.quantity +=1
                    check_cart.save()
                    return JsonResponse({'status':'Sucess', 'message':'Increased the cart quantity', 'cart_counter':get_cart_counter(request)})

                except:
                    check_cart = Cart.objects.create(user=request.user, fooditem=fooditem, qauntity = 1)
                    return JsonResponse({'status':'Sucess', 'message':'Food added to cart!','cart_counter':get_cart_counter(request)})


            except:
                return JsonResponse({'status':'Failed', 'message':'This food does not exist!'})
 
        else:

            return JsonResponse({'status':'Failed', 'message':'Invaild reuest!'})
    else:
        return JsonResponse({'status':'Failed', 'message':'Please login to continue'})
    

def decrease_cart(request, food_id):
    
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with')== 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    check_cart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if check_cart > 1:
                        check_cart.quantity -=1
                        check_cart.save()
                    else:
                        check_cart.delete()
                        check_cart.quantity = 0
                    return JsonResponse({'status': 'Success', 'cart_counter': get_cart_counter(request), 'qty': check_cart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart!'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
        
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})


def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    context = {
        'carrt_items': cart_items,
    }
    return render(request, 'marketplace/cart.html', context)

def delete_cart(request, cart_id):
    if request.user.is_authencitated:
        if request.is_ajax():
            try:
                cart_item = Cart.objects.get(user = request.user, id = cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status':'Success', 'message':'Cart item has deleted!', 'cart_counter': get_cart_counter(request)})
            except:
                return JsonResponse({'status':'Failed', 'message':'Cart items does not exist'})
        else:
            return JsonResponse({'status':'Failed', 'message':'Invalid request!'})
        

def search(request):
    if not 'address' in request.GET:
        return redirect ('marketplace')
    else:
        address = request.GET['address']
        latitude = request.GET['lat']
        longitude = request.GET['lng']
        radius = request.GET['radius']
        keyword = request.GET['keyword']

        fetch_vendors_by_fooditems = FoodItem.objects.filter(food_title__icontains=keyword, is_available=True).values_list('vendor', flat=True)
        
        vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True))

        if latitude and longitude and radius:
            pnt = GEOSGeometry('POINT(%s %s)' %(longitude, latitude))

            vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True),
            user_profile__location__distance_lte=(pnt, D(km=radius))
            ).annotate(distance=Distance("user_profile__location", pnt)).order_by("distance")

            for v in vendors:
                v.kms = round(v.distance.km, 1)

            vendor_count = vendors.count()
        context = {
            'vendor':vendors,
            'vendor_count':vendor_count,
            'source_location': address,
        }

        return render(request, 'marketplace/listings.html', context)