from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import ProjectViewset, ContributorViewset, \
    IssueViewset, CommentViewset, ApiHome


router = routers.SimpleRouter()
router.register('projects', ProjectViewset, basename='project')
router.register('contributors', ContributorViewset, basename='contributor')
router.register('issues', IssueViewset, basename='issue')
router.register('comments', CommentViewset, basename='comment')


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('projects/<int:project_id>/issues/', IssueViewset.as_view(actions={'get': 'list', 'post': 'create'}),
         name='project_issues'),
    path('projects/<int:project_id>/issues/<int:pk>/',
         IssueViewset.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='issue-detail'),
    path('', include('authentication.urls')),
    path('home/', ApiHome.as_view(), name='api_home'),
    path('', include(router.urls)),
]
