from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Project, Issue, Comment
from authentication.serializers import UserSerializer


class ProjectListSerializer(ModelSerializer):
    author_project = serializers.CharField(source='author_project.username', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'author_project']

    def create(self, validated_data):
        request = self.context.get('request')
        current_user = request.user

        contributors = validated_data.get('contributors', [])
        contributors.insert(0, current_user)

        validated_data['author_project'] = current_user
        validated_data['contributors'] = contributors
        validated_data['type'] = self.initial_data.get('type')

        return super().create(validated_data)


class ProjectDetailSerializer(ModelSerializer):
    author_project = serializers.CharField(source='author_project.username', read_only=True)
    contributors = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username')

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
