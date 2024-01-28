from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Project, Issue, Comment
from authentication.serializers import UserSerializer


class ProjectSerializer(ModelSerializer):
    author_project = serializers.CharField(source='author_project.username', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'author_project']

    def create(self, validated_data):
        request = self.context.get('request')
        current_user = request.user
        validated_data['author_project'] = current_user
        validated_data['contributors'] = [current_user]
        return super().create(validated_data)


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
