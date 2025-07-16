

from django.contrib import admin
from django.urls import path, include, re_path # re_path'i import ettik
from django.http import HttpResponse 
from rest_framework import permissions # permissions'ı import ettik
from drf_yasg.views import get_schema_view # get_schema_view'ı import ettik
from drf_yasg import openapi # openapi'yi import ettik

def index(request):
    return HttpResponse("Welcome to User Tracker API! Go to /api/, /swagger/, or /redoc/ for details.")

# Swagger/OpenAPI şemasını oluşturmak için view
schema_view = get_schema_view(
   openapi.Info(
      title="User Tracker API",
      default_version='v1',
      description="Kullanıcıları, gönderilerini, yorumlarını, albümlerini, fotoğraflarını ve görevlerini izlemek için bir API.",
      terms_of_service="https://www.google.com/policies/terms/", # İsteğe bağlı
      contact=openapi.Contact(email="contact@usertracker.local"), # İsteğe bağlı
      license=openapi.License(name="BSD License"), # İsteğe bağlı
   ),
   public=True,
   permission_classes=(permissions.AllowAny,), # Herkesin dokümantasyona erişmesine izin verir
)


urlpatterns = [
    # Ana dizine (/) gelen istekler için basit bir karşılama mesajı
     path('', index, name='index'), # Bu satırı ekledik!
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')), # Kullanıcı uygulamamızın URL'leri

    # drf-yasg (Swagger/OpenAPI) URL'leri
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
