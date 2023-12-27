from unicodedata import name
from django.urls import path, include
from machine_side import views as mv
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('start/', mv.start, name="start_new_mesure"),
    path('add/<slug:msid>/<int:nammount>/', mv.add, name="add_to_mesurement"),
    path('end/<slug:msid>/<int:nammount>/', mv.end, name="end_mesurement"),
    path('archive/monthly/', mv.archive, name="monthly_archive"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)