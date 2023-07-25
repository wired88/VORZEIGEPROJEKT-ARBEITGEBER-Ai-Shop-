from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import BasketHomeView

app_name = 'basket'
urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', BasketHomeView.as_view(), name='basket'),  # legt den home-screen für die basket-app fest
                  path('add/', views.basket_add, name='basket_add'),
                  path('delete/', views.basket_delete, name='basket_delete'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
              static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
