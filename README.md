# Les prénoms en France



Projet individuel Streamlit - EFREI.

Auteur : Bilel BOUDJEMA - Groupe : BIA


## Objectif


Comment les prénoms les plus donnés changent-ils au fil des générations?


Ce Dashboard est pour les étudiants et les personnes curieuses des différentes tendances démographiques. Les filtres permettent de choisir le sexe et la période.


## Installation et lancement


Sous Windows, avec Python 3.12, depuis le dossier du projet:


```

py -3.12 -m venv .venv

.venv\Scripts\activate

python -m pip install -r requirements.txt

python -m streamlit run app.py

```


Ouvrir http://localhost:8501.


Les données sont dans `data/prenoms-2024-nat.zip`.

NE PAS DECOMPRESSER LE FICHIER!



`requirements.txt` donne les versions des bibliothèques.



## Données et méthode



Source : Insee, état civil, fichier national des prénoms, édition

juillet 2025, naissances de 1900 à 2024.



- Catalogue : https://www.data.gouv.fr/datasets/fichier-des-prenoms-depuis-1900

- Fichier : https://www.insee.fr/fr/statistiques/8894961

- Documentation : https://www.insee.fr/fr/statistiques/8894974

- Licence Ouverte 2.0 : https://www.etalab.gouv.fr/licence-ouverte-open-licence/



Colonnes :

- `sexe` : 1 pour masculin, 2 pour féminin

- `prenom` : premier prénom

- `periode` : année de naissance

- `valeur` : effectif arrondi au multiple de 5



Nettoyage : retrait des espaces aux extrémités des prénoms et suppression des doublons exacts.


Validation : sexe 1 ou 2, année de 1900 à 2024, prénom non vide et effectif positif. Les lignes invalides sont exclues.


La section qualité affiche les valeurs manquantes, les doublons et les lignes invalides sur le fichier complet, avant filtrage.


Aucune valeur manquante n'est estimée.


Le classement cumule les effectifs sur la période choisie.


Les égalités sont départagées par ordre alphabétique.



Le top 10 est recalculé chaque année :


Part du top 10 (%) = somme des dix premiers effectifs / total publié de l'année × 100



Les courbes individuelles utilisent le même total annuel, pour le sexe choisi.



## Résultat et limites



Pour les filles, la part du top 10 passe d'environ 23,2 % en 1980 à 8,6 % en 2024. Les prénoms dominants occupent donc une moindre place dans les attributions publiées.


Pour comprendre une mode, il faut comparer les évolutions annuelles au classement cumulé.


Les effectifs sont arrondis. Les prénoms attribués moins de trois fois par sexe et par année ne sont pas publiés donc les totaux et pourcentages concernent uniquement les données publiées.


Les données avant 1946 sont moins complètes.

Mayotte est incluse depuis 2012.


Le fichier porte sur les naissances en France, pas sur la population vivante. Il ne permet ni d'expliquer les causes des tendances ni de prévoir les modes futures.



## Storyboard de la vidéo 


1) Présenter la question, la source et les indicateurs.

2) Montrer le classement des prénoms et survoler les valeurs.

3) Examiner l'évolution du top 10 et comparer les trajectoires.

4) Changer les filtres, puis présenter la conclusion et les limites.

(désolé pour la qualité de mon micro, mais je n'ai pas pu trouver mieux malheureusement)


## Liens de remise


- Application : (https://projet-app-bilel-4jgjvamr2x8f8bcogrc2sy.streamlit.app/)

- Dépôt : (https://github.com/BilelBilelB/projet-streamlit-bilel)

- Vidéo : fichier demo.mp4 joint

