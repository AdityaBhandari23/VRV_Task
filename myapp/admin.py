from django.contrib import admin
from myapp.models import Role, UserRole, Article

admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(Article)
