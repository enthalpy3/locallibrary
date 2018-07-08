from django.conf.urls import url
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'', views.index, name='index'),
    url('books/', views.BookListView.as_view(), name='books'),
    url('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
