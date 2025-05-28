"""
Module pour l'analyse par régression logistique.
"""
import statsmodels.api as sm
import logging

logger = logging.getLogger(__name__)

def fit_logistic_regression(df, features):
    """Ajuste un modèle de régression logistique.
    
    Args:
        df (pandas.DataFrame): DataFrame contenant les données
        features (list): Liste des features à utiliser
        
    Returns:
        statsmodels.regression.linear_model.RegressionResultsWrapper: Modèle ajusté
    """
    logger.info("Ajustement du modèle de régression logistique")
    X = df[features].astype(float)
    y = df['converted']
    
    logit_model = sm.Logit(y, X)
    result = logit_model.fit()
    
    logger.info("Modèle ajusté avec succès")
    return result

def get_model_summary(model):
    """Retourne un résumé du modèle.
    
    Args:
        model (statsmodels.regression.linear_model.RegressionResultsWrapper): Modèle ajusté
        
    Returns:
        str: Résumé du modèle
    """
    return model.summary() 