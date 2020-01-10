from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import (HomeView, 
					CreatePostView, 
					FullArticleView, 
					UpdatePostView, 
					DeletePostView, 
					profile_view, 
					profile_update, 
					profile_pic_update,
                    post_comment)

app_name = 'blog'

urlpatterns = [
    path('', HomeView.as_view(), name='home_view'),
    path('create-post/', CreatePostView.as_view(), name='create_post'),
    path('profile/', profile_view, name='profile_view'),
    path('profile/update', profile_update, name='profile_update'),
    path('profile/pic_update', profile_pic_update, name='profile_pic_update'),
    path('read-full-story/<int:pk>/', FullArticleView.as_view(), name='read_full_story'),
    path('read-full-story/<int:pk>/create-comments/', post_comment, name='create_comment'),
    path('read-full-story/<int:pk>/update', UpdatePostView.as_view(), name='update_post'),
    path('read-full-story/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)