"""IstoryA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from main import views
from django.urls import path

urlpatterns = [
    url(r'^$', views.index),
    url(r'^main/', include('main.urls')),
    url(r'^admin/', admin.site.urls),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('home/', views.homePage, name="home"),
    path('wall/', views.wallPage, name="wall"),
    path('create/<int:id>', views.createPage, name="create"),
    path('order_storyboard/<int:id>', views.createOrderPage, name="create_order"),
    path('update_storyboard/<int:id>', views.updateStoryboard, name="update"),
    path('storyboard/<int:id>', views.viewStoryboard, name="storyboard"),
    path('delete/<int:id>', views.deleteStoryboard, name="delete"),
    path('update_case_storyboard/', views.UpdateCaseStoryboard, name="update_case_storyboard"),
    path('update_case_order_storyboard/', views.UpdateCaseOrderStoryboard, name="update_case_order_storyboard"),
    path('update_list_text', views.updateListText, name="update_list_text"),
    path('fav_storyboard_home/<int:id>', views.favStoryboardHome, name="fav_storyboard_home"),
    path('get_text_by_id/', views.getTextByID, name="get_text_by_id"),
    path('fav_storyboard_publication/<int:id>', views.favStoryboardPublication, name="fav_storyboard_home"),
    path('like_storyboard_publication/<int:id>', views.likeStoryboardPublication, name="like_storyboard_home"),
    path('change_list_create_storyboard/', views.indexListCreateStoryboard, name="change_list_create_storyboard"),
    path('sup/', views.sup, name="sup"),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
