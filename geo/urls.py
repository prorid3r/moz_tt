from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
import test_task.views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny,],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('provider/add', test_task.views.add_provider.as_view()),
    path('provider/<int:pk>/update', test_task.views.update_provider.as_view()),
    path('provider/<int:pk>/get', test_task.views.get_provider.as_view()),
    path('provider/<int:pk>/delete', test_task.views.delete_provider.as_view()),
    path('service-area/add', test_task.views.add_service_area.as_view()),
    path('service-area/<int:pk>/update', test_task.views.update_service_area.as_view()),
    path('service-area/<int:pk>/get', test_task.views.get_service_area.as_view()),
    path('service-area/<int:pk>/delete', test_task.views.delete_service_area.as_view()),
    path('polygons-with-point', test_task.views.polygons_with_point.as_view()),
    re_path(r'^docs/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
