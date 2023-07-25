from django.contrib import admin
from .models import *
# Register your models here.

from django.contrib import admin

from .models import LoadVideoForPageCreation, PictureCategories, GraphicCategory, GraphicUpload, UserAddPicture, User

admin.site.register(LoadVideoForPageCreation)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email', 'password', 'last_login', 'date_created',
                    'profile_image'
                    )


@admin.register(PictureCategories)
class PictureCategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}  # the value of the name field will automaticly given to the slug field


@admin.register(GraphicCategory)
class GraphicCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}  # the value of the name field will automaticly given to the slug field


@admin.register(UserAddPicture)
class UserAddPictureAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'tag_field', 'user_name', 'date', 'slug')  # which fields should show in the django admin area
    prepopulated_fields = {'slug': ('title',)}  # the value of the name field will automaticly given to the slug field
    list_filter = ('is_active', 'tag_field')
    list_editable = ('title', 'price', 'category', 'tag_field')
    list_display_links = ('slug',)


@admin.register(GraphicUpload)
class GraphicUploadAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'price', 'category', 'tag_field', 'g_username', 'date')
    prepopulated_fields = {'slug': ('title',)}  # the value of the name field will automaticly given to the slug field
    list_filter = ('is_active', 'tag_field')  # filter like ' jut show me the active images ...
    list_editable = ('title', 'price', 'category', 'tag_field') # which fields can be edited ......
    list_display_links = ('slug',)
