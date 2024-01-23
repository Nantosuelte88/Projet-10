from django.db import models
from authentication.models import User
import uuid
from django.urls import reverse


class Project (models.Model):
    TYPE_CHOICES = [
        ('back-end', 'Back-end'),
        ('front-end', 'Front-end'),
        ('IOS', 'iOS'),
        ('Android', 'Android'),
    ]

    author_project = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_projects')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True)
    contributors = models.ManyToManyField(User, through='Contributor', related_name='projects')


class Contributor (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Issue (models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Basse'),
        ('MEDIUM', 'Moyenne'),
        ('HIGH', 'Haute'),
    ]

    TAG_CHOICES = [
        ('BUG', 'Erreur'),
        ('FEATURE', 'Fonctionnalité'),
        ('TASK', 'Tâche'),
    ]

    PROGRESS_CHOICES = [
        ('To do', 'A faire'),
        ('In progress', 'En cours'),
        ('Finished', 'Terminé'),
    ]

    author_issue = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_issues')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_issues')
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES)
    tag = models.CharField(max_length=15, choices=TAG_CHOICES)
    progress_status = models.CharField(max_length=15, choices=PROGRESS_CHOICES, default='To do')
    created_on = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    author_comment = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    # faire le lien
