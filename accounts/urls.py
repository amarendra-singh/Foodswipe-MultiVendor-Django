from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.myaccount),
    path('registeruser/', views.registerUser, name='registerUser'),
    path('registervendor/', views.registerVendor, name='registerVendor'),
    
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('customerdashboard/', views.customerDashboard, name='customerDashboard'),
    path('vendordashboard/', views.vendorDashboard, name='vendorDashboard'),
    path('myaccount/', views.myaccount, name='myaccount'),
    
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('vendor/', include('vendor.urls')),
    path('customers/', include('customers.urls'))

]