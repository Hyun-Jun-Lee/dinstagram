from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.generic import RedirectView
from django_pydenticon.urls import image as pydenticon_image



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='instagram:index'), name='root'),
    path('accounts/', include('accounts.urls')),
    path('identicon/image/<path:data>', pydenticon_image, name='pydenticon_image'),
    path('instagram/', include('instagram.urls'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)