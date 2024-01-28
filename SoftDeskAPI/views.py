from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Project, Issue, Comment
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer


class ApiHome(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        message = f"Welcome to the SoftDesk API, {user.username}!"
        return Response({'message': message})


class ProjectViewset(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author_project=self.request.user, contributors=[self.request.user])


class IssueViewset(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]
    # verifier que user est un contributor

    def get_queryset(self):
        return Issue.objects.all()


class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    # verifier que user est un contributor

    def get_queryset(self):
        return Comment.objects.all()
