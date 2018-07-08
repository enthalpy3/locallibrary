from django.conf.urls import include, url
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url('catalog/', include('catalog.urls')),
    url('', RedirectView.as_view(url='/catalog/')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
