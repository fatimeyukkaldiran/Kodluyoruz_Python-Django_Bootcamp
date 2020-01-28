from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from blog import views as blog_views
from blog_user import views as blog_user_views

urlpatterns = [
    path('', blog_views.index, name='home'),

    #USER
    path('accounts/login/', blog_user_views.login_user, name='login'),
    path('accounts/logout/', blog_user_views.logout_user, name='logout'),
    path('accounts/signup/', blog_user_views.sign_up, name='signup'),

    # LIST    
    path('category/<slug:cat_slug>/', blog_views.index, name='cat'),
    path('category/<slug:cat_slug>/<slug:post_slug>/', blog_views.post_detail, name='post_detail'),
    
    # Category
    path('category_list/', blog_views.category_list, name='category_list'),
    path('category_list/action/<int:category_id>/<slug:status>/', blog_views.category_update_status, name='category_delete'),
    path('add-category/', blog_views.add_category, name='add_category'),
    path('add-post/', blog_views.add_post, name='add_post'),

    # PANEL:
    path('panel/', blog_views.panel_list, name='panel'),

    # ACTION:
    path('action/post/love/<int:post_id>/', blog_views.action_post_love, name='post_love'),

    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

