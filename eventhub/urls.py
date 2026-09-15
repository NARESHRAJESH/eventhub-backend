from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.events_api, name='events_api'),
    path('events/<int:id>/', views.event_detail_api, name='event_detail_api'),
    path('bookings/', views.create_booking, name='create_booking'),
    path('organizer/dashboard/', views.organizer_dashboard, name='organizer_dashboard'),
    path('register/', views.register_api, name='register_api'),
    path('login/', views.login_api, name='login_api'),
    path('my-bookings/', views.my_bookings_api, name='my_bookings_api'),
]