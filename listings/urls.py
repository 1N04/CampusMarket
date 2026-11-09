from django.urls import path
from . import views

app_name = 'listings'
urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('item/new/', views.item_create, name='item_create'),
    path('item/<int:pk>/edit/', views.item_edit, name='item_edit'),
    path('item/<int:pk>/delete/', views.item_delete, name='item_delete'),
    path('item/<int:pk>/toggle/', views.item_toggle_availability, name='item_toggle'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<slug:slug>/', views.category_items, name='category'),
]
