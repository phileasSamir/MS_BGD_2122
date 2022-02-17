## Nos scripts

Ce dossier contient l'ensemble des scripts utilisés pour lancer les outils utilisés, charger, et prétraiter les données ainsi que créer les tables Cassandra et les mettre à jour périodiquement.
- ```connect-jupyter.sh```: permet de se connecter sur une machine de TP en redirigeant les ports nécessaires.
- ```start-spark.sh```: permet de lancer Spark avec les paramètres nécessaires.
- ```requests.sql```: contient l'ensemble des requettes SQL/CQL d'agrégation et création des tables, puis de requêtage pour répondre aux questions
- ```scraping``` : regroupe les scripts de téléchargement, nettoyage et chargement dans Cassandra des données :
  - ```get_clean_data.py``` : téléchargement et nettoyage des donnéés
  - ```create_and_load_cassandra.scala``` : agrégation et chargement des donnéés sous Cassandra
  - ```get_latest_data.py``` : téléchargement des derniers fichiers depuis la date du dernier fichier chargé sur le HDFS pour mise à jour périodique de la table.
