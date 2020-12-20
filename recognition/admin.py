from django.contrib import admin
from .models import AdvUser, Company, Order, Tool, ToolType

# Register your models here.
admin.site.register(AdvUser)
admin.site.register(Company)
admin.site.register(Order)
admin.site.register(Tool)
admin.site.register(ToolType)
