# Projet INF728 : NoSQL

Liens vers l'énoncé du TP : http://andreiarion.github.io/Project2022.html.

**La problématique :** L'objectif du projet est de se baser sur la base 2021-2022: GDELT pour répondre à un certain nombre de questions. Pour cela il faut utiliser un système de stockage distribué, résilient et performant.

**Structure du repo :**
- ```config``` : regroupe les fichiers de configuration et commandes utilisés pour installer les outils (Cassandra, Spark, etc.).
- ```scripts``` : regroupe l'ensemble des scripts de récupération, nettoyage des données et la creation des tables sous Cassandra.

**Structure de la base Cassandra :**
La structure de la table Cassandra est détaillée dans le fichier ```scripts/requetes.sql```, voici un bref descriptif :
- ```table_ab``` : extraite à partir des fichiers ```event``` et ```mentions```. Elle contient l'ensemble des données nécessaires pour répondre aux question a et b, et notamment tous les évenements du fichier event, et leurs données relatives (pays, langue, date) mais aussi les dates des mentions associées pour permettre une aggregation par date (année / mois / jour) de mention.
- ```table_c``` :  extraite à partir du fichier ```gkg```. Elle contient l'ensemble des données nécessaires pour répondre à la question c, et notamment les données de source, theme, personne, lieu, date (annee, mois, jour) et des agrégations sur le décompte total et le ton.
- ```table_d``` : extraite à partir du fichier ```gkg```. Elle contient l'ensemble des données nécessaires pour répondre à la question d, et notamment les données de lieu, langue, date (annee, mois, jour) et des agrégations sur le décompte total et le ton.

**Machines utilisées :**
- tp-hadoop-1  (Phileas)
- tp-hadoop-2  (Gwladys)
- tp-hadoop-5  (Pooran)
- tp-hadoop-6  (Jia)
- tp-hadoop-7  (Aurélien)
- tp-hadoop-21 (Pierre)