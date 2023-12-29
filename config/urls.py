from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Habits API Documentation",
        default_version='v1',
        description="Api documentation for Habits API",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="m.donchuk@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path('habits', include('habits.urls', namespace='habits')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
