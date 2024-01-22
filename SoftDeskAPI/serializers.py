from rest_framework.serializers import ModelSerializer
from .models import Project, Issue, Comment


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
