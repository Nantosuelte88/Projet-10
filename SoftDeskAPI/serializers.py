from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Project, Issue, Comment, Contributor
from authentication.models import User
from authentication.serializers import UserSerializer


class ProjectListSerializer(ModelSerializer):
    author_project = serializers.CharField(source='author_project.username', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'author_project']

    def create(self, validated_data):
        request = self.context.get('request')
        current_user = request.user

        validated_data['author_project'] = current_user
        validated_data['contributors'] = [current_user]
        validated_data['type'] = self.initial_data.get('type')

        return super().create(validated_data)


class ProjectDetailSerializer(ModelSerializer):
    author_project = serializers.CharField(source='author_project.username', read_only=True)
    contributors = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username')

    class Meta:
        model = Project
        fields = '__all__'


class ContributorSerializer(ModelSerializer):
    id = serializers.IntegerField(source='user.id', read_only=True)
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Contributor
        fields = ['id', 'user']


class IssueSerializer(serializers.ModelSerializer):
    author_issue = serializers.CharField(source='author_issue.username', read_only=True)
    assigned_to = serializers.SerializerMethodField(read_only=True)

    def get_assigned_to(self, obj):
        if obj.assigned_to:
            return obj.assigned_to.user.username
        return None

    class Meta:
        model = Issue
        fields = '__all__'
        extra_kwargs = {
            'project': {'read_only': True},
        }

    def create(self, validated_data):
        request = self.context['request']
        validated_data['author_issue'] = request.user

        project_id = self.context['view'].kwargs['project_id']
        project = Project.objects.get(id=project_id)
        assigned_to_id = validated_data.get('assigned_to')

        if assigned_to_id:
            contributor = Contributor.objects.filter(user_id=assigned_to_id, project=project)
            if not contributor.exists():
                raise serializers.ValidationError("L'utilisateur assigné n'est pas un contributeur du projet!")

        validated_data['project'] = project
        return super().create(validated_data)


class CommentSerializer(ModelSerializer):
    author_comment = serializers.CharField(source='author_comment.username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'issue': {'read_only': True},
        }

    def create(self, validated_data):
        request = self.context['request']
        validated_data['author_comment'] = request.user

        issue_id = self.context['view'].kwargs['issue_id']
        issue = Issue.objects.get(id=issue_id)

        validated_data['issue'] = issue
        return super().create(validated_data)
