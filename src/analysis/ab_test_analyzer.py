"""
Fonctions d'analyse statistique pour le test A/B.
"""
import pandas as pd
import numpy as np
from statsmodels.stats.proportion import proportions_ztest

def calculate_conversion_rates(df):
    """Calcule les taux de conversion par groupe.
    
    Args:
        df (pandas.DataFrame): DataFrame contenant les données
        
    Returns:
        pandas.Series: Taux de conversion par groupe
    """
    return df.groupby('group')['converted'].mean()

def perform_ab_test(df, alpha=0.05):
    """Effectue le test statistique de comparaison des proportions.
    
    Args:
        df (pandas.DataFrame): DataFrame contenant les données
        alpha (float): Niveau de significativité
        
    Returns:
        dict: Résultats du test statistique
    """
    # Calculer les effectifs
    control_converted = df[(df['group'] == 'control') & (df['converted'] == 1)].shape[0]
    treatment_converted = df[(df['group'] == 'treatment') & (df['converted'] == 1)].shape[0]
    control_total = df[df['group'] == 'control'].shape[0]
    treatment_total = df[df['group'] == 'treatment'].shape[0]
    
    # Effectuer le test
    z_stat, p_value = proportions_ztest(
        [control_converted, treatment_converted],
        [control_total, treatment_total]
    )
    
    # Calculer la différence relative
    control_rate = control_converted / control_total
    treatment_rate = treatment_converted / treatment_total
    relative_difference = ((treatment_rate - control_rate) / control_rate) * 100
    
    return {
        'z_statistic': z_stat,
        'p_value': p_value,
        'significant': p_value < alpha,
        'control_size': control_total,
        'treatment_size': treatment_total,
        'relative_difference': relative_difference
    } 