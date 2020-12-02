from django.urls import path
from general.views import index, ItemView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'general'

urlpatterns = [
      path("", index, name="index"),
      path("item/<str:slug>", ItemView.as_view(), name="item"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # debug
