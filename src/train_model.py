import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score, make_scorer
import os
import joblib
import warnings
import argparse

# Silencia avisos para um output mais limpo
warnings.filterwarnings('ignore')

def train_model(input_path: str, model_output_path: str):
    """
    Carrega dados processados, treina um modelo de regressão logística com
    otimização de hiperparâmetros e salva o melhor modelo.

    Args:
        input_path (str): Caminho para o arquivo CSV com dados processados.
        model_output_path (str): Caminho para salvar o modelo treinado (.pkl).
    """
    print("--- Iniciando o Treinamento do Modelo ---")
    
    # --- 1. Carregar Dados ---
    try:
        df_processed = pd.read_csv(input_path)
        print(f"Dados carregados de '{input_path}' com sucesso.")
    except FileNotFoundError:
        print(f"Erro: Arquivo de dados processados não encontrado em '{input_path}'.")
        return

    # --- 2. Preparar Dados para Treinamento ---
    X = df_processed.drop(columns='Churn')
    y = df_processed['Churn']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Dados divididos em treino ({X_train.shape[0]} amostras) e teste ({X_test.shape[0]} amostras).")

    # --- 3. Otimização de Hiperparâmetros com GridSearchCV ---
    print("Configurando a busca de hiperparâmetros (GridSearch)...")
    
    param_grid = {
        'C': np.logspace(-4, 4, 20),
        'penalty': ['l1', 'l2']
    }
    
    model_base = LogisticRegression(solver='liblinear', random_state=42, class_weight='balanced', max_iter=1000)
    
    scorer_recall = make_scorer(recall_score, pos_label=1)
    
    cv_stratified = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    grid_search = GridSearchCV(
        estimator=model_base,
        param_grid=param_grid,
        scoring=scorer_recall,
        cv=cv_stratified,
        n_jobs=-1,
        verbose=1
    )

    print("Iniciando a busca em grade... Isso pode levar alguns minutos.")
    grid_search.fit(X_train, y_train)

    print("\nBusca em grade concluída!")
    print(f"Melhores parâmetros encontrados: {grid_search.best_params_}")
    print(f"Melhor Recall (validação cruzada): {grid_search.best_score_:.4f}")

    best_model = grid_search.best_estimator_

    # --- 4. Salvar o Modelo Treinado ---
    print(f"Salvando o melhor modelo em '{model_output_path}'...")
    
    output_dir = os.path.dirname(model_output_path)
    os.makedirs(output_dir, exist_ok=True)
    
    joblib.dump(best_model, model_output_path)
    
    print("--- Modelo treinado e salvo com sucesso! ---")


# --- Ponto de Entrada do Script ---
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script para treinar um modelo de Regressão Logística.")
    
    parser.add_argument(
        "--input_path",
        type=str,
        default=os.path.join('..', 'data', '02_processed', 'telco_customer_churn_processed.csv'),
        help="Caminho para o arquivo CSV de dados processados."
    )
    
    parser.add_argument(
        "--output_path",
        type=str,
        default=os.path.join('..', 'models', 'logistic_regression_best_model.pkl'),
        help="Caminho para salvar o modelo treinado (arquivo .pkl)."
    )

    args = parser.parse_args()

    train_model(args.input_path, args.output_path)