"""unmanned_Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from unmanned import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('login/', views.login),
    path('register/', views.register),
    path('profile/', views.get_profile),
    path('profile/record/', views.get_record),
    path('logout/', views.logout),
    path('captcha', include('captcha.urls')),
    path('confirm/', views.user_confirm),
    path('profile/take_pic/', views.take_pic),
    path('upload_image', views.upload_image, name='upload_image'),
    path('test/', views.test_page),
    path('admin_page/', views.admin_report, name='admin_report'),
    path('sales/', views.sales, name='sales'),
    path('admin_page/stock/', views.stock, name='stock'),
    path('admin_page/member_information/', views.member_information, name='member_information'),
    path('admin_page/member_analysis/', views.member_analysis, name='member_analysis'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
