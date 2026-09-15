from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Event, Booking, UserProfile


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'date', 'location', 'price', 'seats')
    list_filter = ('organizer', 'category', 'location')
    search_fields = ('title', 'location')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'event', 'tickets', 'total_amount', 'created_at')
    list_filter = ('event',)
    search_fields = ('customer_name', 'customer_email')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)