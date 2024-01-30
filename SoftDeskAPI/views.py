from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsProjectAuthor, IsIssueAuthor, IsCommentAuthor
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Project, Issue, Comment
from .serializers import ProjectListSerializer, IssueSerializer, \
    CommentSerializer, ProjectDetailSerializer


class ApiHome(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        message = f"Welcome to the SoftDesk API, {user.username}!"
        return Response({'message': message})


class ProjectViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsProjectAuthor]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        contributors = self.request.data.get('contributors', '')
        contributors = [contributor.strip() for contributor in contributors.split(',')]
        contributors.insert(0, self.request.user)
        serializer.save(author_project=self.request.user, contributors=contributors)


class IssueViewset(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Issue.objects.all()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsIssueAuthor]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]


class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.all()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsCommentAuthor]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]
