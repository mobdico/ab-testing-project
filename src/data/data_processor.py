"""
Fonctions de traitement des données pour l'analyse A/B.
"""
import pandas as pd
import logging
from datetime import datetime
import os

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_processing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_data(file_path):
    """Charge les données depuis le fichier CSV.
    
    Args:
        file_path (str): Chemin vers le fichier CSV
        
    Returns:
        pandas.DataFrame: DataFrame contenant les données
    """
    logger.info(f"Chargement des données depuis {file_path}")
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Données chargées avec succès : {len(df)} lignes")
        return df
    except Exception as e:
        logger.error(f"Erreur lors du chargement des données : {str(e)}")
        raise

def clean_data(df):
    """Nettoie les données en supprimant les incohérences.
    
    Args:
        df (pandas.DataFrame): DataFrame à nettoyer
        
    Returns:
        pandas.DataFrame: DataFrame nettoyé
    """
    logger.info("Début du nettoyage des données")
    initial_rows = len(df)
    
    # Supprimer les utilisateurs dans le mauvais groupe
    df = df.drop(df[(df['group'] == 'control') & (df['landing_page'] == 'new_page')].index)
    df = df.drop(df[(df['group'] == 'treatment') & (df['landing_page'] == 'old_page')].index)
    
    removed_rows = initial_rows - len(df)
    logger.info(f"Nettoyage terminé : {removed_rows} lignes supprimées")
    return df

def remove_duplicates(df):
    """Supprime les utilisateurs en double.
    
    Args:
        df (pandas.DataFrame): DataFrame à nettoyer
        
    Returns:
        pandas.DataFrame: DataFrame sans doublons
    """
    logger.info("Suppression des doublons")
    initial_rows = len(df)
    df = df.drop_duplicates(subset=['user_id'])
    removed_rows = initial_rows - len(df)
    logger.info(f"Doublons supprimés : {removed_rows} lignes")
    return df

def save_processed_data(df, output_dir, filename=None):
    """Sauvegarde les données nettoyées.
    
    Args:
        df (pandas.DataFrame): DataFrame à sauvegarder
        output_dir (str): Répertoire de sortie
        filename (str, optional): Nom du fichier de sortie
        
    Returns:
        str: Chemin du fichier sauvegardé
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"processed_data_{timestamp}.csv"
    
    output_path = os.path.join(output_dir, filename)
    logger.info(f"Sauvegarde des données nettoyées dans {output_path}")
    
    try:
        df.to_csv(output_path, index=False)
        logger.info(f"Données sauvegardées avec succès : {len(df)} lignes")
        return output_path
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde des données : {str(e)}")
        raise

def compare_raw_processed(raw_df, processed_df):
    """Compare les données brutes et nettoyées.
    
    Args:
        raw_df (pandas.DataFrame): Données brutes
        processed_df (pandas.DataFrame): Données nettoyées
        
    Returns:
        dict: Statistiques de comparaison
    """
    logger.info("Comparaison des données brutes et nettoyées")
    
    # Statistiques de base
    stats = {
        'raw_rows': len(raw_df),
        'processed_rows': len(processed_df),
        'removed_rows': len(raw_df) - len(processed_df),
        'removal_percentage': ((len(raw_df) - len(processed_df)) / len(raw_df)) * 100
    }
    
    # Analyse des incohérences
    control_new_page = len(raw_df[(raw_df['group'] == 'control') & (raw_df['landing_page'] == 'new_page')])
    treatment_old_page = len(raw_df[(raw_df['group'] == 'treatment') & (raw_df['landing_page'] == 'old_page')])
    
    stats['inconsistencies'] = {
        'control_new_page': control_new_page,
        'treatment_old_page': treatment_old_page,
        'total_inconsistencies': control_new_page + treatment_old_page
    }
    
    # Analyse des doublons
    duplicates = raw_df['user_id'].duplicated().sum()
    stats['duplicates'] = duplicates
    
    # Taux de conversion
    stats['conversion_rates'] = {
        'raw': raw_df.groupby('group')['converted'].mean().to_dict(),
        'processed': processed_df.groupby('group')['converted'].mean().to_dict()
    }
    
    logger.info(f"Comparaison terminée : {stats['removed_rows']} lignes supprimées ({stats['removal_percentage']:.2f}%)")
    return stats 

def prepare_features(df):
    """Prépare les features pour l'analyse.
    
    Args:
        df (pandas.DataFrame): DataFrame à préparer
        
    Returns:
        pandas.DataFrame: DataFrame avec les features préparées
    """
    logger.info("Préparation des features")
    
    # Convertir timestamp en datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.day_name()
    
    # One-hot encoding des jours de la semaine
    day_dummies = pd.get_dummies(df['day_of_week'], prefix='day', drop_first=False)
    df = pd.concat([df, day_dummies], axis=1)
    
    # Créer la variable binaire pour le groupe
    df['ab_group'] = df['group'].map({'control': 0, 'treatment': 1})
    df['intercept'] = 1
    
    logger.info("Features préparées avec succès")
    return df 