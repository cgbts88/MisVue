from django.urls import path, include
from apps.system.views_index import IndexView, LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

	path('', IndexView.as_view(), name='index'),
	path('login/', LoginView.as_view(), name='login'),
	path('logout/', LogoutView.as_view(), name='logout'),

	path('system/', include(('system.urls', 'system'), namespace='system')),
	path('worktable/', include(('worktable.urls', 'worktable'), namespace='worktable')),
	path('personnel/', include(('users.urls', 'personnel'), namespace='personnel')),
	path('asset/', include(('asset.urls', 'asset'), namespace='asset')),

	path('api-auth/', include('rest_framework.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


