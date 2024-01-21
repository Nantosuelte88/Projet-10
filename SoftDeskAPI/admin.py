from django.contrib import admin
from django.utils.html import format_html
from .models import Project, Issue, Comment
from authentication.models import User


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'author_project', 'get_contributors', 'name', 'description', 'type', 'created_on')

    def get_contributors(self, obj):
        return ", ".join([contributor.username for contributor in obj.contributors.all()])

    get_contributors.short_description = 'Contributors'


admin.site.register(User)

admin.site.register(Project, ProjectAdmin)
