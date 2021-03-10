from django.urls import path, include
from system.views.index import UserAuthView
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html")),

    path('system/', include(('system.urls', 'system'), namespace='system')),
    path('worktable/', include(('worktable.urls', 'worktable'), namespace='worktable')),
    path('personnel/', include(('users.urls', 'personnel'), namespace='personnel')),
    path('asset/', include(('asset.urls', 'asset'), namespace='asset')),

    # path('api-auth/', include('rest_framework.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
