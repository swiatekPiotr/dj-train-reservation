from django.contrib import admin
from .models import Course, Station, Timetable, Carriage, Seating


@admin.register(Course)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ["id", "start", "end"]


@admin.register(Station)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Timetable)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ["lp_station", "stations", "courses"]
    list_filter = ["courses"]


@admin.register(Carriage)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ["id", "courses"]


@admin.register(Seating)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ["id", "carriages"]
