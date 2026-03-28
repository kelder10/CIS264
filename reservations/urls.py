from django.urls import path
from . import views

urlpatterns = [
    path('check-availability/', views.check_availability, name='check_availability'),
    path('create/<slug:bike_slug>/', views.create_reservation, name='create_reservation'),
    path('waiver/<int:reservation_id>/', views.waiver, name='waiver'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
    path('detail/<int:pk>/', views.reservation_detail, name='reservation_detail'),
    path('cancel/<int:pk>/', views.cancel_reservation, name='cancel_reservation'),
    path('confirmation/<int:pk>/', views.reservation_confirmation, name='reservation_confirmation'),
]
