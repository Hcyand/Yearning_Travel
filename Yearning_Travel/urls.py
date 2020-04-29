"""Yearning_Travel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from login import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  path('', views.index),
                  path('admin/', admin.site.urls),
                  path('index/', views.index),
                  path('login/', views.login),
                  path('register/', views.register),
                  path('logout/', views.logout),
                  path('search/', views.search),
                  path('profile/', views.profile),
                  path('article/', views.article),
                  path('buy/', views.buy),
                  path('buy_detail/', views.buy_detail),
                  path('hot_discussion/', views.hot_discussion),
                  path('comment_discussion/', views.comment_discussion),
                  path('recommend/', views.recommend),
                  path('recommend_scenery/', views.recommend_scenery),
                  path('recommend_article/', views.recommend_article),
                  path('book/', views.book),
                  path('scenery/', views.scenery),
                  path('scenery_look/', views.scenery_look),
                  path('like_up/', views.like_up),
                  path('personality/', views.personality),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
