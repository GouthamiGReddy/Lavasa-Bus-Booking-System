from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('book/<int:slot_id>/', views.book_slot, name='book_slot'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

    # Admin URLs
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/slots/add/', views.admin_add_slot, name='admin_add_slot'),
    path('admin/slots/<int:slot_id>/edit/', views.admin_edit_slot, name='admin_edit_slot'),
    path('admin/slots/<int:slot_id>/delete/', views.admin_delete_slot, name='admin_delete_slot'),
    path('admin/slots/<int:slot_id>/bookings/', views.admin_slot_bookings, name='admin_slot_bookings'),
    path('admin/bookings/<int:booking_id>/action/', views.admin_booking_action, name='admin_booking_action'),
    path('admin/users/', views.admin_users, name='admin_users'),
]
