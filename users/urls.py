from django.contrib.auth import views
from django.urls import include, path
from . import views
from .views import ProfileDetailView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('profile/', ProfileDetailView.as_view(), name='profile'),
    path('settings/', views.settings, name='settings'),
]
