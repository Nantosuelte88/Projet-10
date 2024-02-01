from rest_framework.permissions import BasePermission
from .models import Project


class IsProjectAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author_project == request.user


class IsIssueAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author_issue == request.user


class IsCommentAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author_comment == request.user


class IsProjectContributor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.contributors.filter(id=request.user.id).exists()


class IsProjectForIssueContributor(BasePermission):
    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_id')
        project = Project.objects.get(id=project_id)
        return project.contributors.filter(id=request.user.id).exists()
