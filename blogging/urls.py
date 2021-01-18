from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.PostList.as_view(), name="index"),
    path('details/<slug:slug>', views.PostDetailView.as_view(), name="post_detail"),
    path('save/post/', views.PostCreateView.as_view(), name="save_post"),
    path('update/post/<slug:slug>', views.PostUpdateView.as_view(), name="update_post"),
    path('delete/post/<slug:slug>', views.PostDeleteView.as_view(), name="delete_post"),
    path('login/user/', views.UserLoginView.as_view(), name="user_login"),
    path('create/user/', views.CreateUserProfile.as_view(), name="create_user"),
    path('logout', views.user_logout, name="user_logout"),
    path('user/<str:username>', views.UserDetailView.as_view(), name="user_profile"),
    path('update/user/<str:username>', views.UserUpdateView.as_view(), name="update_user_profile"),
    path('categories/', views.categories, name="categories_list"),
    path('category/<str:name>', views.category_detail, name="category_detail"),
    path('category/post/<int:id>', views.category_post, name="category_post"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)