from django.urls import path,include
from .views import home,registration,unauthorized_access,user_login
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('',home,name='home'),
    path('registration/',registration,name='registration'),
    path('404/',unauthorized_access,name='404'),
    path('user_login/',user_login,name='user_login'),


    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)