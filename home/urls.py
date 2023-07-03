from django.contrib import admin
from django.http import request
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from . import views
from .views import HomeView, RegisterView, UserLoginView, ProfileView, SettingsView, \
    UserAddPicture, PictureDetailView, logout_view, delete_object_view, \
    DeleteObjectView, delete_object_view, UsersImagesListView, UserAddPictureView

app_name = 'home'
urlpatterns = [
                  path('', HomeView.as_view(), name='index'),
                  path('register/', RegisterView.as_view(), name='register'),

                  path('login/', UserLoginView.as_view(), name='login'),
                  path('description/', TemplateView.as_view(template_name='home/description.html'), name='description'),
                  path('logout/', logout_view, name='logout'),

                  # detailes Picture View from profile
                  path('user-picture/<slug:slug>/<int:pk>/', PictureDetailView.as_view(), name='user-picture'),
                  # evtl error wegen slug<. slug da slug in models = title

                  # <pk> is identification for id field,
                  # slug can also be used
                  # <int:product_id>/ hier wird das Parameter in das base.html file übergeben, damit django weiß, welches Produkt
                  # gelöscht werden soll
                  path('delete/<int:pk>/', views.delete_object_view, name='delete'),
                  #  path('delete/<int:pk>/', delete_grocery_view(), name='delete'),
                  # path('delete-recipe/<int:pk>/', delete_object_view, name='delete-recipe'),
                  # value = models.IntegerField()

                  # Listed pictures View from Profile
                  path('my-images/', UsersImagesListView.as_view(), name='my-images'),
                  # for profile/my imges (private view)

                  path('create/', UserAddPictureView.as_view(), name='create'),
                  path('settings/', SettingsView.as_view(), name='settings'),
                  path('profile/', ProfileView.as_view(), name="profile"),

                  # path('password/', auth_views.PasswordChangeView.as_view(), name='password'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
              static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
