from django.contrib import admin

from .models import UserProfile, Chrono

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ("user", 'tel', 'email', 'fonction')

class ChronoAdmin(admin.ModelAdmin):
	list_display = ("prefixe", "fonctionalite", "annee", "mois", "nombre", "last_chrono")

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Chrono, ChronoAdmin)
