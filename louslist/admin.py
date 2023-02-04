from django.contrib import admin, auth
from django.contrib.auth.models import User

# Register your models here.

from .models import uva_class, uva_dept, users, friendRequest, friendship, comment

class uva_class_admin(admin.ModelAdmin):
    fieldsets = []

class uva_dept_admin(admin.ModelAdmin):
    fieldsets = []



class friendRequest_admin(admin.ModelAdmin):
    fieldsets = []

class friendship_admin(admin.ModelAdmin):
    fieldsets = []

class comment_admin(admin.ModelAdmin):
    fieldsets = []

admin.site.register(uva_class, uva_class_admin)
admin.site.register(uva_dept,uva_dept_admin)
admin.site.register(friendRequest, friendRequest_admin)
admin.site.register(friendship, friendship_admin)
admin.site.register(users)
admin.site.register(comment,comment_admin)
