import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, roc_curve
import os
import joblib
import argparse
import warnings

# Silencia avisos para um output mais limpo
warnings.filterwarnings('ignore')

def evaluate_model(model_path: str, data_path: str, roc_data_path: str, coefficients_path: str):
    """
    Carrega um modelo treinado e dados para avaliar o desempenho no conjunto de teste.
    Salva métricas e artefatos de interpretabilidade.

    Args:
        model_path (str): Caminho para o modelo treinado (.pkl).
        data_path (str): Caminho para os dados processados (.csv).
        roc_data_path (str): Caminho para salvar os dados da curva ROC (.csv).
        coefficients_path (str): Caminho para salvar os coeficientes do modelo (.csv).
    """
    print("--- Iniciando a Avaliação do Modelo ---")

    # --- 1. Carregar Modelo e Dados ---
    try:
        model = joblib.load(model_path)
        print(f"Modelo carregado de '{model_path}'.")
    except FileNotFoundError:
        print(f"Erro: Arquivo de modelo não encontrado em '{model_path}'.")
        return

    try:
        df_processed = pd.read_csv(data_path)
        print(f"Dados carregados de '{data_path}'.")
    except FileNotFoundError:
        print(f"Erro: Arquivo de dados não encontrado em '{data_path}'.")
        return

    # --- 2. Preparar Dados de Teste ---
    X = df_processed.drop(columns='Churn')
    y = df_processed['Churn']
    
    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print("Conjunto de teste recriado com sucesso.")

    # --- 3. Fazer Predições e Avaliar ---
    print("\nAvaliando o modelo no conjunto de TESTE...")
    
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    print("\nRelatório de Classificação (TESTE):")
    print(classification_report(y_test, y_pred))

    auc_score = roc_auc_score(y_test, y_prob)
    print(f"Pontuação AUC-ROC (TESTE): {auc_score:.4f}")

    # --- 4. Gerar e Salvar Artefatos de Avaliação ---

    # a) Dados da Curva ROC para Dashboard
    print(f"Salvando os dados da Curva ROC em '{roc_data_path}'...")
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    df_roc_data = pd.DataFrame({'FPR': fpr, 'TPR': tpr})
    
    os.makedirs(os.path.dirname(roc_data_path), exist_ok=True)
    df_roc_data.to_csv(roc_data_path, index=False)

    # b) Coeficientes do Modelo para Interpretabilidade
    print(f"Salvando os coeficientes do modelo em '{coefficients_path}'...")
    coeficientes = model.coef_[0]
    features = X.columns
    
    df_coeficientes = pd.DataFrame({'Atributo': features, 'Coeficiente': coeficientes})
    df_coeficientes_ordenado = df_coeficientes.reindex(df_coeficientes['Coeficiente'].abs().sort_values(ascending=False).index)
    
    os.makedirs(os.path.dirname(coefficients_path), exist_ok=True)
    df_coeficientes_ordenado.to_csv(coefficients_path, index=False)
    
    print("\n--- Avaliação concluída e artefatos salvos! ---")


# --- Ponto de Entrada do Script ---
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script para avaliar um modelo de classificação treinado.")
    
    parser.add_argument(
        "--model_path",
        type=str,
        default=os.path.join('..', 'models', 'logistic_regression_best_model.pkl'),
        help="Caminho para o modelo treinado (.pkl)."
    )
    
    parser.add_argument(
        "--data_path",
        type=str,
        default=os.path.join('..', 'data', '02_processed', 'telco_customer_churn_processed.csv'),
        help="Caminho para o arquivo CSV de dados processados."
    )

    # REMOVIDO: O argumento para salvar o gráfico da curva ROC
    # parser.add_argument("--roc_plot_path", ...)
    
    parser.add_argument(
        "--roc_data_path",
        type=str,
        default=os.path.join('..', 'reports', 'dashboard_data', 'roc_curve_data.csv'),
        help="Caminho para salvar os dados da curva ROC (.csv)."
    )

    # ADICIONADO: O argumento para salvar os coeficientes do modelo
    parser.add_argument(
        "--coefficients_path",
        type=str,
        default=os.path.join('..', 'reports', 'dashboard_data', 'logistic_regression_coefficients.csv'),
        help="Caminho para salvar os coeficientes do modelo (.csv)."
    )

    args = parser.parse_args()
    evaluate_model(args.model_path, args.data_path, args.roc_data_path, args.coefficients_path)