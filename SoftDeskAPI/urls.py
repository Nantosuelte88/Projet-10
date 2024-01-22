from django.urls import path, include
from rest_framework import routers

from .views import ProjectViewset, IssueViewset, CommentViewset, api_home

router = routers.SimpleRouter()
router.register('projects', ProjectViewset, basename='project')
router.register('issues', IssueViewset, basename='issue')
router.register('comments', CommentViewset, basename='comment')


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', api_home, name='api_home'),
    path('', include(router.urls)),
]
