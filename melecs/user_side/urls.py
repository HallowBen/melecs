from unicodedata import name
from django.urls import path, include
from user_side import views as sv
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', sv.home, name="home"),
    path('home_chart/', sv.home_chart, name="home_chart"),
    path('test/', sv.test, name="test"),
    path('measurements/', sv.allms, name="all meassurement base"),
    path('msdata/<str:order>', sv.msdata, name="all meassurement data"),
    path('msdetails/<slug:msid>/', sv.detailms, name="detailed meassurement"),
    path('mssearch/<str:where>/<str:what>', sv.mssearch, name="searched meassurement"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)