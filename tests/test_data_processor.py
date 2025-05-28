"""
Tests unitaires pour le module data_processor.
"""
import os
import sys
import pytest
import pandas as pd

# Ajouter le répertoire parent au PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.data.data_processor import load_data, clean_data, remove_duplicates

# Données de test
TEST_DATA = pd.DataFrame({
    'user_id': [1, 2, 3, 4, 5],
    'timestamp': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'],
    'group': ['control', 'treatment', 'control', 'treatment', 'control'],
    'landing_page': ['old_page', 'new_page', 'old_page', 'new_page', 'new_page'],
    'converted': [0, 1, 0, 1, 0]
})

def test_load_data():
    """Test de la fonction load_data."""
    # Créer un fichier temporaire pour le test
    test_file = os.path.join(project_root, 'tests', 'test_data.csv')
    TEST_DATA.to_csv(test_file, index=False)
    
    try:
        # Tester le chargement
        df = load_data(test_file)
        assert len(df) == len(TEST_DATA)
        assert all(col in df.columns for col in TEST_DATA.columns)
    finally:
        # Nettoyer le fichier temporaire
        if os.path.exists(test_file):
            os.remove(test_file)

def test_clean_data():
    """Test de la fonction clean_data."""
    # Données avec des incohérences
    df = TEST_DATA.copy()
    df.loc[0, 'landing_page'] = 'new_page'  # Incohérence : control avec new_page
    
    # Nettoyage
    cleaned_df = clean_data(df)
    
    # Vérifications
    assert len(cleaned_df) < len(df)  # Des lignes ont été supprimées
    assert not any((cleaned_df['group'] == 'control') & (cleaned_df['landing_page'] == 'new_page'))
    assert not any((cleaned_df['group'] == 'treatment') & (cleaned_df['landing_page'] == 'old_page'))

def test_remove_duplicates():
    """Test de la fonction remove_duplicates."""
    # Données avec des doublons
    df = TEST_DATA.copy()
    df = pd.concat([df, df.iloc[0:2]])  # Ajout de doublons
    
    # Suppression des doublons
    deduped_df = remove_duplicates(df)
    
    # Vérifications
    assert len(deduped_df) == len(TEST_DATA)
    assert deduped_df['user_id'].nunique() == len(TEST_DATA)

def test_data_structure():
    """Test de la structure des dossiers."""
    # Vérifier l'existence des dossiers
    assert os.path.exists(os.path.join(project_root, 'datasets', 'raw'))
    assert os.path.exists(os.path.join(project_root, 'datasets', 'processed'))
    assert os.path.exists(os.path.join(project_root, 'src', 'data'))
    assert os.path.exists(os.path.join(project_root, 'src', 'analysis'))
    assert os.path.exists(os.path.join(project_root, 'src', 'visualization'))

if __name__ == '__main__':
    # Exécuter les tests quand le fichier est lancé directement
    pytest.main([__file__, '-v']) 