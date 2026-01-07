from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('reports/', include('reports.urls')),
    path('moderation/', include('moderation.urls')),
    path('panel/', include('admin_panel.urls')),
    path('awareness/', include('awareness.urls')),
    path('', lambda request: redirect('user_dashboard') if request.user.is_authenticated else redirect('login'), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
