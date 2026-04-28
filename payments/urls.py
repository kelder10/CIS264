from django.urls import path
from . import views

urlpatterns = [
    path('process/<int:reservation_id>/', views.payment, name='payment'),
    path('confirmation/<int:payment_id>/', views.payment_confirmation, name='payment_confirmation'),
    path('history/', views.payment_history, name='payment_history'),
    path('apply-promo/<int:reservation_id>/', views.apply_promo_code, name='apply_promo_code'),
]
