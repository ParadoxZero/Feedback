from django.contrib import admin

# Register your models here.

class FeedbackUserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, 'generate')
    ]