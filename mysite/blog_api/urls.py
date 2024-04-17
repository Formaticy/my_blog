from django.urls import path, re_path
from drf_spectacular.views import SpectacularAPIView

from .views import PostDetail, PostList, UserPostList

urlpatterns = [
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('', PostList.as_view(), name='post_list'),
    re_path('^user/(?P<id>.+)/$', UserPostList.as_view()),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
]