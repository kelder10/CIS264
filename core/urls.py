from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('trails/', views.trails, name='trails'),
    path('contact/', views.contact, name='contact'),
    path('api/weather/', views.weather_api, name='weather_api'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path("admin-dashboard/bikes/", views.admin_bikes, name="admin_bikes"),
    path("admin-dashboard/bikes/<int:bike_id>/toggle-availability/", views.toggle_bike_availability, name="toggle_bike_availability"),
    path("admin-dashboard/bikes/<int:bike_id>/toggle-maintenance/", views.toggle_bike_maintenance, name="toggle_bike_maintenance"),

    path("admin-dashboard/reservations/", views.admin_reservations, name="admin_reservations"),
    path("admin-dashboard/reservations/<int:reservation_id>/status/<str:new_status>/", views.update_reservation_status, name="update_reservation_status"),

    path("admin-dashboard/reviews/", views.admin_reviews, name="admin_reviews"),
    path("admin-dashboard/reviews/<int:review_id>/approve/", views.approve_review, name="approve_review"),
    path("admin-dashboard/reviews/<int:review_id>/unapprove/", views.unapprove_review, name="unapprove_review"),

    path("admin-dashboard/payments/", views.admin_payments, name="admin_payments"),
    path("admin-dashboard/payments/<int:payment_id>/refund/", views.refund_payment, name="refund_payment"),
    path("admin-dashboard/payments/<int:payment_id>/void/", views.void_payment, name="void_payment"),
]
