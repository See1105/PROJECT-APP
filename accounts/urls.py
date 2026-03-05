from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import SignUpView, DashboardView, SettingsView, DeleteAccountView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete_account'),
]
