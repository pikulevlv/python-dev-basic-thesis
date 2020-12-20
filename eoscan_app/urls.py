from django.contrib import admin
from django.urls import path,  include
from django.conf.urls.static import static
from django.conf import settings

import debug_toolbar
import captcha

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recognition.urls', namespace='recognition')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('captcha/', include('captcha.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.THUMBNAIL_MEDIA_URL,
                          document_root=settings.THUMBNAIL_MEDIA_ROOT)
