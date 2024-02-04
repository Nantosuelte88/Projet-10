from django.contrib import admin
from .models import Project
from authentication.models import User


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'author_project', 'get_contributors', 'name', 'description', 'type', 'created_on')

    def get_contributors(self, obj):
        # Méthode pour obtenir les noms des contributeurs sous forme d'une chaîne de caractères séparée par des virgules
        return ", ".join([contributor.username for contributor in obj.contributors.all()])
    get_contributors.short_description = 'Contributors'


# Enregistrement des modèles dans l'administration
admin.site.register(User)
admin.site.register(Project, ProjectAdmin)
