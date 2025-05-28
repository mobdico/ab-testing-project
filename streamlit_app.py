"""
Application Streamlit pour l'analyse A/B.
"""
import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Ajouter le répertoire racine au PYTHONPATH
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Importer les modules
from src.data import data_processor
from src.analysis.ab_test_analyzer import calculate_conversion_rates, perform_ab_test
from src.visualization.streamlit_plots import (
    plot_conversion_rates,
    plot_statistical_results,
    plot_conversion_by_hour,
    plot_conversion_by_day
)

# Définition des chemins
RAW_DATA_DIR = Path(project_root) / 'datasets' / 'raw'
PROCESSED_DATA_DIR = Path(project_root) / 'datasets' / 'processed'
RAW_DATA_FILE = RAW_DATA_DIR / 'ab_data.csv'

# Configuration de la page
st.set_page_config(
    page_title="Analyse de Test A/B",
    page_icon="📊",
    layout="wide"
)

# Section "À propos" dans la barre latérale
with st.sidebar:
    st.title("À propos")
    st.write("Cette application a été développée par :")
    
    # Premier développeur
    st.markdown("""
        <div style='text-align: center; margin: 10px 0;'>
            <a href='https://www.linkedin.com/in/mamadou-oury-balde-4270301ab/' target='_blank' style='text-decoration: none; color: #0077B5;'>
                <h3 style='margin: 0;'>Mamadou Oury Baldé</h3>
            </a>
        </div>
    """, unsafe_allow_html=True)
    
    # Deuxième développeur
    st.markdown("""
        <div style='text-align: center; margin: 10px 0;'>
            <a href='https://www.linkedin.com/in/ernest-aounang/' target='_blank' style='text-decoration: none; color: #0077B5;'>
                <h3 style='margin: 0;'>Ernest Aounang</h3>
            </a>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")  # Séparateur

# Titre de l'application
st.title("Analyse de Test A/B")

# Vérifier si le fichier de données existe
if not RAW_DATA_FILE.exists():
    st.error(f"Le fichier de données n'existe pas : {RAW_DATA_FILE}")
    st.stop()

# Charger les données
df = data_processor.load_data(RAW_DATA_FILE)

# Nettoyer les données
df_cleaned = data_processor.clean_data(df)

# Supprimer les doublons
df_final = data_processor.remove_duplicates(df_cleaned)

# Afficher les informations sur les données
st.write("### Informations sur les données")
st.write(f"Nombre total d'observations : {len(df_final)}")
st.write(f"Nombre de doublons supprimés : {len(df) - len(df_final)}")

# Calculer les taux de conversion
conversion_rates = calculate_conversion_rates(df_final)

# Afficher les taux de conversion
st.write("### Taux de Conversion par Groupe")
plot_conversion_rates(conversion_rates)

# Effectuer le test statistique
test_results = perform_ab_test(df_final)

# Afficher les résultats statistiques
plot_statistical_results(test_results)

# Afficher les graphiques temporels
st.write("### Analyse Temporelle")
plot_conversion_by_hour(df_final)
plot_conversion_by_day(df_final)

# Bouton pour sauvegarder les données nettoyées
if st.sidebar.button("Sauvegarder les données nettoyées"):
    output_path = data_processor.save_processed_data(df_final, PROCESSED_DATA_DIR)
    st.sidebar.success(f"Données sauvegardées dans {output_path}") 