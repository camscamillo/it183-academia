from django.urls import path
from .views import (
    blog_list,
    blog_detail,
    blog_delete,
    blog_create,
    blog_update,
    like_post,
    user_login,
    user_signup,
    user_logout,
)
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
urlpatterns = [
    path('api/', include(router.urls)),  # Include all router URLs
    path('', blog_list, name='blog_list'),  # Home page showing the list of blogs
    path('create/', blog_create, name='blog_create'),  # Create a new post
    path('<int:id>/update/', blog_update, name='blog_update'),  # Update a specific post
    path('<int:post_id>/', blog_detail, name='blog_detail'),  # Updated to use post_id
    path('<int:id>/delete/', blog_delete, name='blog_delete'),  # Delete a specific post
    path('post/<int:post_id>/like/', like_post, name='like_post'),  # Like a specific post
    path('login/', user_login, name='login'),  # User login
    path('signup/', user_signup, name='signup'),  # User signup
    path('logout/', user_logout, name='logout'),  # User logout
]
