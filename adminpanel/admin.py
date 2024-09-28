from django.contrib import admin
from .models import Profile,Comment_Table,Blog_Table

# Register your models here.
admin.site.register(Profile)
admin.site.register(Blog_Table)
admin.site.register(Comment_Table)