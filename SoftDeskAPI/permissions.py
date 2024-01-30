from rest_framework.permissions import BasePermission


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
        return obj.contributor == request.user
