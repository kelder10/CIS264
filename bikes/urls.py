from django.urls import path
from . import views


urlpatterns = [
    path('', views.bike_list, name='bike_list'),
    path('sizes/', views.bike_sizes_guide, name='bike_sizes'),
    path('accessories/', views.accessories_list, name='accessories'),
    path('accessories/add/<int:accessory_id>/', views.add_accessory, name='add_accessory'),
    path('adults/', views.adult_bikes, name='adult_bikes'),
    path('kids/', views.kids_bikes, name='kids_bikes'),
    path('mountain/', views.mountain_bikes, name='mountain_bikes'),
    path('category/<slug:slug>/', views.bike_category, name='bike_category'),
    path('<slug:slug>/', views.bike_detail, name='bike_detail'),
    path('admin-dashboard/fleet-dispatch/', views.fleet_dispatch, name='fleet_dispatch'),
    path('admin-dashboard/pickup/<int:location_id>/', views.confirm_pickup, name='confirm_pickup'),
]
