from django.urls import path, include
from .views import registro_usuario
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("registro/", registro_usuario, name="registro_usuario"),
    path('', include('django.contrib.auth.urls')),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
]
