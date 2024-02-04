from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


def validate_age(date_of_birth):
    # Définit la limite d'âge comme 15 ans avant la date actuelle
    age_limit = timezone.now() - timedelta(days=15 * 365)

    if date_of_birth > age_limit.date():
        raise ValidationError("Vous devez avoir au moins 15 ans pour créer un compte.")


class User(AbstractUser):
    # Modèle utilisateur personnalisé qui étend la classe AbstractUser de Django avec des champs supplémentaires
    date_of_birth = models.DateField(validators=[validate_age])
    can_be_contacted = models.BooleanField(default=True)
    can_data_be_shared = models.BooleanField(default=True)

