from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from authentication.views import custom_404_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('auth/', include('authentication.urls')),
    path('api/', include('apis.urls')),
    path('chat/', include('chat.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = custom_404_view
handler403 = custom_404_view
handler400 = custom_404_view


