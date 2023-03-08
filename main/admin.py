from django.contrib import admin

from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('date_time_start', 'date_time_end', 'category', 'reservation', 'on_main')


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('rank',)


@admin.register(models.Reservations)
class ReservationsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'update_at')
    readonly_fields = ('created_at',)

