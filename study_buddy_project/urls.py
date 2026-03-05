from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('study/', include('study.urls')),
    path('ai/', include('ai_buddy.urls')),
    path('collaboration/', include('collaboration.urls')),
    path('video/', include('video_buddy.urls')),
    path('', HomeView.as_view(), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
