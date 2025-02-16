from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from blog.views import PostListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PostListView.as_view(), name='home'),
    path('blog/', include('blog.urls', namespace='blog')),
    path('users/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

# The static() helper function is suitable for development but not for production use.
# Django is very inefficient at serving static files. Never serve your static files with Django
# in a production environment. You will learn how to serve static files in a production environment
# in Chapter 17, Going Live.
