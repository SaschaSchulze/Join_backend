"""
URL configuration for join_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from join.views import register_user, login_user, get_users, set_item, get_item

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', register_user, name='register_user'),
    path('api/login/', login_user, name='login_user'),
    path('api/data/users/', get_users, name='get_users'),
    path('api/set-item/', set_item, name='set_item'),  # Neue Route für setItem
    path('api/get-item/', get_item, name='get_item'),  # Neue Route für getItem
]
