
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="index"),
    path('download',views.download,name="download"),
    path('download_final',views.download_content_final,name="download_final"),
    path('terms',views.terms,name="terms"),
    path('privacy',views.privacy,name='privacy'),
    path('save_feedback',views.save_feedback,name="save_feedback")
]


urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)