from rest_framework.permissions import BasePermission
from .models import Project


class IsProjectAuthor(BasePermission):
    # Vérifie si l'utilisateur est l'auteur du projet
    def has_object_permission(self, request, view, obj):
        return obj.author_project == request.user


class IsIssueAuthor(BasePermission):
    # Vérifie si l'utilisateur est l'auteur de l'issue
    def has_object_permission(self, request, view, obj):
        return obj.author_issue == request.user


class IsCommentAuthor(BasePermission):
    # Vérifie si l'utilisateur est l'auteur du commentaire
    def has_object_permission(self, request, view, obj):
        return obj.author_comment == request.user


class IsProjectContributor(BasePermission):
    # Vérifie si l'utilisateur est un contributeur du projet
    def has_object_permission(self, request, view, obj):
        return obj.contributors.filter(id=request.user.id).exists()


class IsProjectForIssueContributor(BasePermission):
    # Vérifie si l'utilisateur est un contributeur du projet pour l'issue en cours
    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_id')
        project = Project.objects.get(id=project_id)
        return project.contributors.filter(id=request.user.id).exists()
