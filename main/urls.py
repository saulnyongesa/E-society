"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from base import views
from base.forms import PWDChangeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
]
# Password and account related urls===========================================
urlpatterns += [
    path('password-change/', PWDChangeView.as_view(template_name='pwd/pwd-change.html'), name='change-pwd-url'),
    path('reset_pwd/', auth_views.PasswordResetView.as_view(template_name='pwd/pwd-reset.html'),
         name='reset_password'),
    path('reset_pwd_done/',
         auth_views.PasswordResetDoneView.as_view(template_name='pwd/done.html'),
         name='password_reset_done'),
    path('reset_pwd/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='pwd/confirm.html'),
         name='password_reset_confirm'),
    path('reset_pwd_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='pwd/complete.html'),
         name='password_reset_complete'),
    path('account/verify/<int:id>/', views.otp_verify, name='verify-url')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
