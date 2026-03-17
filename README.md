# Web Scraping Books to Scrape

Ce projet permet d'extraire les données du site Books to Scrape et de générer
un fichier CSV par catégorie ainsi que les images des livres.

## Description

Ce script Python extrait les informations des livres du site Books to Scrape.

Pour chaque catégorie :
- toutes les pages sont parcourues
- les informations des livres sont récupérées
- un fichier CSV est généré
- les images des livres sont téléchargées

## Données extraites

Les informations suivantes sont récupérées :

- UPC
- Title
- Price including tax
- Price excluding tax
- Number available
- Description
- Category
- Review rating
- Image URL
- Image

## Installation

Cloner le projet 
Puis créer un environnement virtuel 

    pyenv activate py3.10

Puis télécharger les requirements

    pip install -r requirements.txt

## Exécution

    python book_to_scrape.py


