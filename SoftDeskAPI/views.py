from rest_framework import status
from rest_framework import serializers
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated
from .permissions import IsProjectAuthor, IsIssueAuthor, \
    IsCommentAuthor, IsProjectContributor, IsProjectForIssueContributor

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Project, Issue, Comment, User, Contributor
from .serializers import ProjectListSerializer, ContributorSerializer,\
    IssueSerializer, CommentSerializer, ProjectDetailSerializer


class ApiHome(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        message = f"Welcome to the SoftDesk API, {user.username}!"
        return Response({'message': message})


class ProjectViewset(ModelViewSet):
    # Classe pour gérer les vues relatives aux projets

    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_serializer_class(self):
        # Renvoie la classe de sérialiseur en fonction de l'action
        if self.action in ['retrieve', 'update', 'partial_update']:
            return self.detail_serializer_class
        return super().get_serializer_class()

    def get_permissions(self):
        # Renvoie la liste des classes de permissions en fonction de l'action
        if self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsProjectContributor]
        elif self.action in ['update', 'partial_update', 'destroy', 'contributors']:
            permission_classes = [IsAuthenticated, IsProjectAuthor]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # Crée un nouveau projet avec l'utilisateur actuel comme auteur et
        # ajout de l'utilisateur actuel comme contributeur
        project = serializer.save(author_project=self.request.user)
        project.contributors.add(self.request.user)

    def get_contributors_queryset(self):
        # Renvoie le queryset des contributeurs pour le projet actuel
        project = self.get_object()
        return Contributor.objects.filter(project=project)

    @action(detail=True, methods=['get', 'post', 'patch', 'delete'], url_path='contributors')
    # Vue personnalisée pour gérer les contributeurs d'un projet
    def contributors(self, request, pk=None):
        project = self.get_object()

        if request.method == 'GET':
            # Récupère la liste des contributeurs pour le projet et les sérialise
            contributors = self.get_contributors_queryset()
            serializer = ContributorSerializer(contributors, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            # Ajoute un contributeur au projet
            contributor_username = request.data.get('username')
            if contributor_username:
                contributor = User.objects.get(username=contributor_username)
                project.contributors.add(contributor)
                return Response({'message': 'Contributor added successfully.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Invalid username.'}, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PATCH':
            # Supprime un contributeur du projet
            contributor_username = request.data.get('username')
            if contributor_username:
                contributor = User.objects.get(username=contributor_username)
                project.contributors.remove(contributor)
                return Response({'message': 'Contributor removed successfully.'})
            else:
                return Response({'error': 'Invalid username.'}, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            # Supprime un contributeur du projet
            contributor_username = request.data.get('username')
            if contributor_username:
                contributor = User.objects.get(username=contributor_username)
                project.contributors.remove(contributor)
                return Response({'message': 'Contributor removed successfully.'})
            else:
                return Response({'error': 'Invalid username.'}, status=status.HTTP_400_BAD_REQUEST)


class ContributorViewset(ModelViewSet):
    # Classe pour gérer les vues relatives aux contributeurs
    permission_classes = [IsAuthenticated]
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer


class IssueViewset(ModelViewSet):
    # Classe pour gérer les vues relatives aux issues

    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsProjectForIssueContributor]

    def get_queryset(self):
        # Récupère les objets Issue associés au projet spécifié dans les paramètres de l'URL
        project_id = self.kwargs['project_id']
        return Issue.objects.filter(project_id=project_id)

    def create(self, request, *args, **kwargs):
        # Crée une nouvelle issue pour le projet spécifié dans les paramètres de l'URL
        project_id = self.kwargs['project_id']
        project = Project.objects.get(id=project_id)
        assigned_to_id = self.request.data.get('assigned_to')

        if assigned_to_id:
            contributor = Contributor.objects.filter(user_id=assigned_to_id, project=project)
            if not contributor.exists():
                raise serializers.ValidationError("L'utilisateur assigné n'est pas un contributeur du projet!")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author_issue=self.request.user, project=project)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_update(self, serializer):
        # Met à jour une issue existante et vérifie si l'utilisateur assigné est un contributeur du projet
        issue = self.get_object()  # Récupérer l'instance de l'issue à mettre à jour
        assigned_to_id = self.request.data.get('assigned_to')
        project_id = issue.project_id

        if assigned_to_id:
            contributor = Contributor.objects.filter(user_id=assigned_to_id, project_id=project_id)
            if not contributor.exists():
                raise serializers.ValidationError(
                    "L'utilisateur assigné n'est pas un contributeur du projet correspondant.")

            contributor_instance = contributor.first()
            serializer.save(assigned_to=contributor_instance)
        else:
            serializer.save()

    def get_permissions(self):
        # Définit les autorisations requises en fonction de l'action demandée
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsIssueAuthor]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated, IsProjectForIssueContributor]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]


class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsProjectForIssueContributor]

    def get_queryset(self):
        # Récupère les commentaires associés à l'issue spécifiée dans les paramètres de l'URL
        project_id = self.kwargs['project_id']
        issue_id = self.kwargs['issue_id']
        return Comment.objects.filter(issue__project_id=project_id, issue_id=issue_id)

    def retrieve(self, request, *args, **kwargs):
        # Récupère et renvoie un commentaire spécifique
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # Crée un nouveau commentaire pour l'issue spécifiée dans les paramètres de l'URL
        issue_id = self.kwargs['issue_id']
        issue = Issue.objects.get(id=issue_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author_comment=self.request.user, issue=issue)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_permissions(self):
        # Définit les autorisations requises en fonction de l'action demandée
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsCommentAuthor]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated, IsProjectForIssueContributor]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]
