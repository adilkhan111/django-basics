from django.contrib import admin
from .models import Post, UserProfile, Categories
# Register your models here.
@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'author', 'slug', 'created_on', 'last_modified']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [ 'user', 'profile_img', 'dob', 'qualification']

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
