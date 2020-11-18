"""SocialMedia URL Configuration

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
from connect.views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Login,name="login"),
    path('in/<str:Username>/',UserProfile,name="userProfile"),
    path('register/',Register,name="register"),
    path('logout/', Logout, name="logout"),
    path('in/editUserDetails/<str:Username>/', Edit_User_Details, name="editUserDetails"),
    path('connections/<str:action>/<int:u_id>/',Manage_connections,name="connections"),
    path('company/',Add_Company,name="company"),
    path('professionals/<str:what>/',Professionals,name="professionals"),
    path('company_blogs/',Company_Blogs,name="companyBlogs"),
    path('companies_detail/',Companies_Detail,name="companies_detail"),
    path('likes/<int:b_id>/<str:Username>/',Likes,name="likes"),
    path('comments/<int:b_id>/<str:Username>/',Comments,name="comments"),
    path('see_comments/<int:b_id>/<str:Username>/', See_Comments, name="see_comments"),
    path('baseData/',Base_Data,name="baseData"),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
