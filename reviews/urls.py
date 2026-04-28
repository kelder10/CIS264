from django.urls import path
from . import views

urlpatterns = [
    path('', views.review_list, name='reviews'),
    path('submit/', views.submit_review, name='submit_review'),
    path('detail/<int:pk>/', views.review_detail, name='review_detail'),
    path('edit/<int:pk>/', views.edit_review, name='edit_review'),
    path('delete/<int:pk>/', views.delete_review, name='delete_review'),
    path('helpful/<int:pk>/', views.mark_helpful, name='mark_helpful'),
]
