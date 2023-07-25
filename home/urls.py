from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from . import views
from .views import HomeView, RegisterView, UserLoginView, ProfileView, SettingsView, PictureDetailView, logout_view, \
    UsersImagesListView, UserAddPictureView, PictureUpdateView, CustomerDetailView, CategoryView, SingleCategoyView

app_name = 'home'
urlpatterns = [

                  # HOMEVIEW
                  path('', HomeView.as_view(), name='index'),

                  # DESCRIPTION PAGES
                  # Description (whats going on this website?)
                  path('description/', TemplateView.as_view(template_name='home/description.html'), name='description'),

                  # SIGN IN / SIGN UP / SIGN OUT
                  # Sign In
                  path('login/', UserLoginView.as_view(), name='login'),

                  # Sign Up
                  path('register/', RegisterView.as_view(), name='register'),

                  # logout
                  path('logout/', logout_view, name='logout'),

                  # CATEGORY VIEWS
                  # Graphic
                  path('categories/', CategoryView.as_view(), name='category'),

                  # Picture

                  # VIEWS FOR SINGLE CATEGORY
                  # Graphic

                  path('category/<slug:slug>/', SingleCategoyView.as_view(), name='category_single'),

                  # Picture DETAIL VIEW
                  path('image/<slug:slug>', CustomerDetailView.as_view(), name='customer_detail_view'),

                  # MY-IMAGES VIEW
                  # Graphic and Picture ListView
                  path('my-images/', UsersImagesListView.as_view(), name='my-images'),

                  # Graphic and Picture detail
                  path('user-picture/<int:pk>/<slug:slug>/', PictureDetailView.as_view(), name='user-picture'),

                  # UPDATE VIEW
                  path('edit-image/<int:pk>/<slug:slug>/', PictureUpdateView.as_view(), name='edit-image'),

                  # DELETE VIEW
                  path('delete/<int:pk>/', views.delete_object_view, name='delete'),

                  # CREATE VIEW
                  path('create/', UserAddPictureView.as_view(), name='create'),
                  # Todo Graphic #

                  # PROFILE AND SETTINGS
                  # Profile
                  path('profile/<int:pk>/', ProfileView.as_view(), name="profile"),

                  # Settings
                  path('settings/', SettingsView.as_view(), name='settings'),

                  # for media and static load
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
              static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
