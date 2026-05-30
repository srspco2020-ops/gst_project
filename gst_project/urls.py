from django.urls import path
from django.contrib import admin
from invoice.views import (
    gstin_list,
    gstin_detail,
    register_view,
    login_view,
    logout_view,
    dashboard_view,
    base_view,
    public_gstin_data
)

urlpatterns = [
    # Authentication URLs
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # Application URLs
    path('gstin_list', gstin_list, name='gstin_list'),  # Homepage
    path('gstin/<str:gstin>/', gstin_detail, name='gstin_detail'),
    path('', base_view, name='base'),
    
    # Uncomment when you need admin
     path('admin/', admin.site.urls),
     path('public-table/', public_gstin_data, name='public_table'),
]