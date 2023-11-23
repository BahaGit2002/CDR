from django.contrib import admin
from CDR.models import CDR, User


@admin.register(CDR)
class CDRAdmin(admin.ModelAdmin):
    list_display = ('call_id', 'calling_number')
    list_display_links = list_display


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    list_display_links = list_display
