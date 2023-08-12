from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 路由转发
    path('admin/', admin.site.urls),
    path('webops/', include(('webops.urls', 'webops'), namespace='webops')),
]
