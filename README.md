# Projet-10


### Prérequis

Vous devez avoir Django installé, en amont vous trouverez de plus amples informations concernant Django sur [ce lien](https://www.djangoproject.com/) ou [GitHub de Django](https://github.com/django/django).
Ainsi que Django Django REST framework installé, [site offciel](https://www.django-rest-framework.org/) ou [GitHub de Django-rest-framework](https://github.com/encode/django-rest-framework).

> [!IMPORTANT]
> Nécessite une version de Python supérieure à 3


## Installation

Avant tout, installer pip env si il ne l'est pas déjà :
```
$ pip install pipenv
```


Clonez le projet : 
```
$ git clone https://github.com/Nantosuelte88/Projet-10.git
```


Pour créer l'environnement :
```
$ pipenv install
```

Pour l'activer sur Unix et MacOS :
```
$ pipenv shell
```

Installez les dépendances :
```
$ pip install -r requirements.txt
```

Appliquez les migrations :
```
$ python manage.py migrate
```

Lancez le serveur
```
$ python manage.py runserver
```

