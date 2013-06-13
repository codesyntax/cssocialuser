from django.contrib import admin
from django.db import models
from django.conf import settings
AUTH_PROFILE_MODULE = getattr(settings,'AUTH_PROFILE_MODULE', 'cssocialuser.CSSocialUser')
"""
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', )
    search_fields = ['user__username',]

app_label, model_name = AUTH_PROFILE_MODULE.split('.') 
model = models.get_model(app_label, model_name)

admin.site.register(model,UserProfileAdmin)
"""
