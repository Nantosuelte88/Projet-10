# Generated by Django 5.0.1 on 2024-01-22 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SoftDeskAPI', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='issue_link',
        ),
    ]