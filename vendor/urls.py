from django.urls import path, include
from . import views
from accounts import views as accountViews


urlpatterns = [
    path('', accountViews.vendorDashboard, name='vendor'),
    path('profile/', views.vprofile, name='vprofile'),
    path('menu-builder/', views.menu_builder, name='menu_builder'),

]