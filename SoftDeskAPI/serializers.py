from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Project, Issue, Comment, Contributor


class ProjectListSerializer(ModelSerializer):
    # Serializer pour la liste des projets

    # Champ pour afficher le nom d'utilisateur de l'auteur du projet
    author_project = serializers.CharField(source='author_project.username', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'author_project', 'description']

    def create(self, validated_data):
        # Méthode pour créer un nouveau projet

        # Récupérer la requête en cours depuis le contexte
        request = self.context.get('request')
        current_user = request.user

        # Définir l'auteur du projet comme l'utilisateur actuel et l'ajoute aux contributeurs
        validated_data['author_project'] = current_user
        validated_data['contributors'] = [current_user]
        validated_data['type'] = self.initial_data.get('type')

        return super().create(validated_data)


class ProjectDetailSerializer(ModelSerializer):
    # Serializer pour les détails d'un projet

    # Champs pour afficher le nom d'utilisateur de l'auteur du projet et les contributeurs du projet
    author_project = serializers.CharField(source='author_project.username', read_only=True)
    contributors = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username')

    class Meta:
        model = Project
        fields = '__all__'


class ContributorSerializer(ModelSerializer):
    # Serializer pour les contributeurs

    # Champs pour l'ID et le nom d'utilisateur de l'utilisateur
    id = serializers.IntegerField(source='user.id', read_only=True)
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Contributor
        fields = ['id', 'user']


class IssueSerializer(serializers.ModelSerializer):
    # Serializer pour les problèmes (issues)

    # Champ pour afficher le nom d'utilisateur de l'auteur du problème
    author_issue = serializers.CharField(source='author_issue.username', read_only=True)

    # Champ pour afficher le nom d'utilisateur de l'utilisateur assigné au problème
    assigned_to = serializers.SerializerMethodField(read_only=True)

    def get_assigned_to(self, obj):
        # Méthode pour obtenir le nom d'utilisateur de l'utilisateur assigné
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
        # Méthode pour créer un nouveau problème
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
    # Serializer pour les commentaires

    # Champ pour afficher le nom d'utilisateur de l'auteur du commentaire
    author_comment = serializers.CharField(source='author_comment.username', read_only=True)

    # Champ pour obtenir le lien du projet lié au commentaire
    project_link = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'issue': {'read_only': True},
        }

    def get_project_link(self, obj):
        # Méthode pour obtenir le lien du projet lié au commentaire
        request = self.context.get('request')
        if request is not None:
            path = f'/api/projects/{obj.issue.project_id}/'
            return request.build_absolute_uri(path)
        return None

    def to_representation(self, instance):
        # Méthode pour personnaliser la représentation des données
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request is not None:
            data['project_link'] = self.get_project_link(instance)
        return data

    def create(self, validated_data):
        # Méthode pour créer un nouveau commentaire
        request = self.context['request']
        validated_data['author_comment'] = request.user

        issue_id = self.context['view'].kwargs['issue_id']
        issue = Issue.objects.get(id=issue_id)

        validated_data['issue'] = issue
        return super().create(validated_data)
