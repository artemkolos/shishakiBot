from django.contrib import admin

# Register your models here.
from .models import Category_group,Category,Service,ServiceReport

admin.site.register(Category_group)
admin.site.register(Category)
admin.site.register(Service)
admin.site.register(ServiceReport)
