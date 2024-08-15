from django.urls import path
from . import views 

urlpatterns = [
    path('',views.post_list,name='post_list'),
    path('<slug:slug>',views.full_post,name='full_post'),
    path('bloglist/upload',views.upload_blog,name='upload_blog'),
    path('tags/<int:specific_tag>',views.tagged_blog,name='tagged_blog'),
]