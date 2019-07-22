from django.conf.urls import url
from django.urls import include

from . import views
from django.conf import settings
from django.conf.urls.static import static
import notifications.urls

urlpatterns = [
    url('^notifications/', include(notifications.urls, namespace='notifications')),
    url(r'^$', views.index, name='posts'),
    url(r'^posts/create$', views.create_post, name='posts.create'),
    url(r'^login$', views.login_view, name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^posts/(?P<id>\d+)/show/$', views.show_post, name='posts.show'),
    url(r'^categories/$', views.category, name='categories'),
    url(r'^categories/create$', views.create_category, name='categories.create'),
    url(r'categories/delete/(?P<id>\d+)', views.delete_category, name='categories.delete'),
    url(r'categories/(?P<name>[\w\-]+)/post/$', views.show_category_post, name='categories.show_post'),
    url(r'^categories/edit/(?P<id>\d+)', views.edit_category, name='categories.edit'),
    url(r'^categories/update/(?P<id>\d+)', views.update_category, name='categories.update'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
