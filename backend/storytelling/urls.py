from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/", include("stories.urls")),
]

if settings.SERVE_FRONTEND_FROM_DJANGO:
    urlpatterns += [
        path("", TemplateView.as_view(template_name="index.html"), name="spa-root"),
        re_path(r"^(?!api/|admin/).*$", TemplateView.as_view(template_name="index.html"), name="spa-fallback"),
    ]
