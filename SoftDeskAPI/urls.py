from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import ProjectViewset, ContributorViewset, \
    IssueViewset, CommentViewset


# Création d'un routeur pour les vues basées sur ViewSet
router = routers.SimpleRouter()
router.register('projects', ProjectViewset, basename='project')
router.register('contributors', ContributorViewset, basename='contributor')
router.register('issues', IssueViewset, basename='issue')
router.register('comments', CommentViewset, basename='comment')


urlpatterns = [
    # URLs pour l'authentification de l'API
    path('api-auth/', include('rest_framework.urls')),
    path('', include('authentication.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # URLs pour les actions liées aux projets aux issues et aux commentaires
    path('projects/<int:project_id>/issues/',
         IssueViewset.as_view(actions={'get': 'list', 'post': 'create'}), name='project_issues'),
    path('projects/<int:project_id>/issues/<int:pk>/',
         IssueViewset.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='issue-detail'),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/',
         CommentViewset.as_view({'get': 'list', 'post': 'create'}), name='comment-list'),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/<int:pk>/',
         CommentViewset.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='comment-detail'),

    # URLs générées par le routeur pour les vues basées sur ViewSet
    path('', include(router.urls)),
]
