from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'Crescent University'
admin.site.index_title = 'Crescent Dashboard'

urlpatterns = [
    path('', include('cert_app.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)