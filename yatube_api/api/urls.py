from django.urls import include, path
from rest_framework import routers

from .views import CommentViewSet, FollowList, GroupViewSet, PostViewSet

router_api_01 = routers.DefaultRouter()
router_api_01.register('posts', PostViewSet, basename='posts')
router_api_01.register(r'posts/(?P<post_id>\d+)/comments',
                       CommentViewSet, basename='comments')
router_api_01.register('groups', GroupViewSet, basename='groups')

urlpatterns = [
    path('v1/', include(router_api_01.urls)),
    path('v1/follow/', FollowList.as_view()),
    path('v1/', include('djoser.urls.jwt')),
]
