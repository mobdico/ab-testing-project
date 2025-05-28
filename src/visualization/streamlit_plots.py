"""
Fonctions de visualisation pour l'interface Streamlit.
"""
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_conversion_rates(conversion_rates):
    """Crée un graphique des taux de conversion.
    
    Args:
        conversion_rates (pandas.Series): Taux de conversion par groupe
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    conversion_rates.plot(kind='bar', ax=ax)
    ax.set_title('Taux de Conversion par Groupe')
    ax.set_ylabel('Taux de Conversion')
    ax.set_xlabel('Groupe')
    st.pyplot(fig)

def plot_statistical_results(test_results):
    """Affiche les résultats statistiques.
    
    Args:
        test_results (dict): Résultats du test statistique
    """
    st.write("### Résultats du Test Statistique")
    st.write(f"Statistique Z : {test_results['z_statistic']:.4f}")
    st.write(f"P-valeur : {test_results['p_value']:.4f}")
    st.write(f"Résultat significatif : {'Oui' if test_results['significant'] else 'Non'}")

def plot_conversion_by_hour(df):
    """Crée un graphique des taux de conversion par heure.
    
    Args:
        df (pandas.DataFrame): DataFrame contenant les données
    """
    # Extraire l'heure à partir de la colonne timestamp
    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    
    # Calculer les taux de conversion moyens par heure et par groupe
    hourly_rates = df.groupby(['hour', 'group'])['converted'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=hourly_rates, x='hour', y='converted', hue='group', ax=ax)
    ax.set_title('Taux de Conversion par Heure')
    ax.set_xlabel('Heure')
    ax.set_ylabel('Taux de Conversion')
    st.pyplot(fig)

def plot_conversion_by_day(df):
    """Crée un graphique des taux de conversion par jour de la semaine.
    
    Args:
        df (pandas.DataFrame): DataFrame contenant les données
    """
    # Extraire le jour de la semaine à partir de la colonne timestamp
    df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.day_name()
    
    # Calculer les taux de conversion moyens par jour et par groupe
    daily_rates = df.groupby(['day_of_week', 'group'])['converted'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=daily_rates, x='day_of_week', y='converted', hue='group', ax=ax)
    ax.set_title('Taux de Conversion par Jour de la Semaine')
    ax.set_xlabel('Jour de la semaine')
    ax.set_ylabel('Taux de Conversion')
    plt.xticks(rotation=45)
    st.pyplot(fig) 