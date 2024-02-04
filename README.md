# Projet-10


<div align="center">
  <img alt="Logo de JustStreamIt" src="https://github.com/Nantosuelte88/Projet-10/blob/main/media/logo.png" width="300px">
</div>
<p align="center">
    “Découvrez SoftDesk Support, notre application B2B innovante pour remonter et suivre vos problèmes techniques avec facilité.”
</p>

## Pour commencer

Ce projet est créé dans le cadre de la formation de Développeur d'application Python proposée par [OpenClassrooms](https://openclassrooms.com/fr/).

### Le projet

Créer un moyen standard de traiter les données en développant une API RESTful. 

### Les exigences :
  + Créer une API RESTful en utilisant Django Rest Framework.
  + Suivre le fichier de conception de la mise en œuvre.
  + Utiliser Pipenv pour gérer les dépendances.
  + Respecter les normes de sécurité OWASP.
  + Respecter les normes de protection des données personnelles RGPD.
  + Respecter les directives de codage de la PEP8 pour assurer la lisibilité du code.




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

Appliquez les migrations :
```
$ python manage.py migrate
```

Lancez le serveur
```
$ python manage.py runserver
```



### Fonctionnalités

L'API offre plusieurs fonctionnalités :

1. **Créer un compte :**
   - Vous pouvez créer un compte en fournissant un pseudo, un mot de passe et votre date de naissance (Veuillez noter que le site est réservé aux personnes de 15 ans et plus).
   - Vous pouvez spécifier si vous souhaitez être contacté(e) et si vous autorisez le partage de vos données (ces préférences sont modifiables ultérieurement).

2. **Créer un Projet :**
   - Vous pouvez créer un projet pour une application cliente. Lors de la création du projet, vous pouvez lui donner un nom, une description et spécifier son type (back-end, front-end, iOS ou Android).
   - Vous pouvez ajouter des contributeurs à votre projet. Ils pourront voir les détails du projet, créer des "issues" (tâches/problèmes) et les commenter.

3. **Créer une Issue :**
   - En tant que contributeur du projet, vous pouvez participer activement au projet en créant une issue (tâche/problème). Les issues permettent de planifier les fonctionnalités à implémenter ou les bogues à résoudre dans un projet donné.
   - Vous pouvez attribuer une issue à un autre contributeur du projet, si vous le souhaitez.
   - Vous pouvez donner une priorité à l'issue (LOW, MEDIUM ou HIGH) pour indiquer son importance.
   - Vous pouvez également ajouter une balise (BUG, FEATURE ou TASK) pour spécifier la nature de l'issue.
   - Vous pouvez également définir un statut de progression (To Do, In Progress ou Finished).

4. **Créer des commentaires :**
   - Pour mieux comprendre les problèmes et faciliter la communication, les contributeurs d'un projet peuvent commenter les issues de ce projet en utilisant les commentaires.

Explorez les fonctionnalités puissantes de notre API qui vous permettent de créer des comptes, de développer des projets, de résoudre des problèmes et de collaborer de manière transparente. Maximisez votre productivité et améliorez votre expérience de gestion de projet grâce à notre plateforme innovante.



## Langages Utilisés

* Python - framework Django
* Django Rest Framework


  
> README rédigé à l'aide de :
> - [Docs GitHub](https://docs.github.com/fr/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
> - [Template by PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
> - [Align items by DavidWells](https://gist.github.com/DavidWells/7d2e0e1bc78f4ac59a123ddf8b74932d)




