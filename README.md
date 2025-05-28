# Projet d'Analyse A/B Testing

Ce projet permet d'effectuer une analyse A/B test sur des données de conversion de landing pages.

## Structure du Projet

```
ab-testing-project/
│
├── data/                      # Dossier contenant les données
│   ├── raw/                  # Données brutes originales
│   │   └── ab_data.csv      # Fichier CSV des données brutes
│   └── processed/           # Données nettoyées et prêtes pour l'analyse
│       └── processed_data.csv # Données après nettoyage
│
├── src/                      # Code source du projet
│   ├── data/                # Code de traitement des données
│   │   ├── __init__.py
│   │   └── data_processor.py # Fonctions de nettoyage et préparation
│   │
│   ├── analysis/            # Code d'analyse statistique
│   │   ├── __init__.py
│   │   └── ab_test_analyzer.py # Fonctions d'analyse A/B
│   │
│   └── visualization/       # Code de visualisation
│       ├── __init__.py
│       └── streamlit_plots.py # Fonctions de visualisation Streamlit
│
├── notebooks/               # Notebooks Jupyter
│   └── Projet_A_B_testing.ipynb # Notebook d'analyse original
│
├── tests/                  # Tests unitaires
│
├── streamlit_app.py        # Application Streamlit
├── requirements.txt        # Dépendances Python
└── README.md              # Documentation
```

## Installation

1. Cloner le repository
2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
```
3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

1. Placer le fichier de données brutes dans `data/raw/ab_data.csv`
2. Lancer l'application Streamlit :
```bash
streamlit run streamlit_app.py
```

## Fonctionnalités

- Nettoyage automatique des données
- Analyse statistique des taux de conversion
- Visualisation interactive des résultats
- Test d'hypothèse avec niveau de significativité ajustable

## Structure des Données

Le fichier CSV doit contenir les colonnes suivantes :
- user_id : identifiant unique de l'utilisateur
- timestamp : date et heure de l'interaction
- group : groupe de test (control/treatment)
- landing_page : page de destination (old_page/new_page)
- converted : résultat de la conversion (0/1)

## Résultats

Les résultats de l'analyse seront disponibles dans le dossier `