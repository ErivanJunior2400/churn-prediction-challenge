import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, MinMaxScaler, PowerTransformer, StandardScaler
import numpy as np
import os
import argparse
import warnings

# Silencia avisos para um output mais limpo no terminal
warnings.filterwarnings('ignore')

def preprocess_data(input_path: str, output_path: str):
    """
    Carrega dados brutos, aplica um pipeline de pré-processamento e salva o resultado.

    Args:
        input_path (str): Caminho para o arquivo CSV de entrada (dados brutos).
        output_path (str): Caminho para salvar o arquivo CSV de saída (dados processados).
    """
    print(f"Iniciando o pré-processamento dos dados de '{input_path}'...")
    
    # --- 1. Carregar e Limpar os Dados ---
    try:
        df = pd.read_csv(input_path, delimiter=';')
    except FileNotFoundError:
        print(f"Erro: O arquivo '{input_path}' não foi encontrado. Verifique o caminho.")
        return

    # Definir listas de colunas
    colunas_para_remover = ['customerID']
    colunas_label_encoding = ['Dependents', 'Partner', 'PhoneService', 'PaperlessBilling', 'gender', 'Contract']
    colunas_one_hot_encoding = ['OnlineSecurity', 'StreamingMovies', 'OnlineBackup', 'StreamingTV', 'MultipleLines', 'DeviceProtection', 'TechSupport', 'InternetService', 'PaymentMethod']
    coluna_alvo = 'Churn'
    colunas_numericas_escalar = ['tenure', 'MonthlyCharges']
    coluna_para_transformar = 'TotalCharges'

    # Remove a coluna customerID
    if all(col in df.columns for col in colunas_para_remover):
        df = df.drop(columns=colunas_para_remover, axis=1)

    # Converte colunas numéricas e trata valores nulos
    for col in ['MonthlyCharges', 'TotalCharges', 'tenure']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        if df[col].isnull().sum() > 0:
            valor_mediana = df[col].median()
            df[col].fillna(valor_mediana, inplace=True)
            print(f"Valores nulos em '{col}' preenchidos com a mediana: {valor_mediana}")

    # 2. Trata nulos em colunas CATEGÓRICAS com a MODA
    colunas_categoricas = colunas_label_encoding + colunas_one_hot_encoding
    for col in colunas_categoricas:
        # Checa se a coluna realmente existe no DataFrame antes de tentar acessá-la
        if col in df.columns and df[col].isnull().sum() > 0:
            # .mode() retorna uma Series, então pegamos o primeiro valor com [0]
            valor_moda = df[col].mode()[0] 
            df[col].fillna(valor_moda, inplace=True)
            print(f"Valores nulos em '{col}' preenchidos com a moda: {valor_moda}")


    # --- 2. Engenharia de Atributos e Codificação ---

    # Inicializa o DataFrame processado
    df_processado = pd.DataFrame()

    # Aplica Label Encoding
    for col in colunas_label_encoding:
        from sklearn.preprocessing import LabelEncoder
        codificador_rotulos = LabelEncoder()
        df_processado[col] = codificador_rotulos.fit_transform(df[col])

    # Aplica One-Hot Encoding e converte para int
    from sklearn.preprocessing import OneHotEncoder
    codificador_ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    transformado_ohe = codificador_ohe.fit_transform(df[colunas_one_hot_encoding])
    transformado_ohe = transformado_ohe.astype(int)
    df_ohe = pd.DataFrame(transformado_ohe, columns=codificador_ohe.get_feature_names_out(colunas_one_hot_encoding), index=df.index)
    df_processado = pd.concat([df_processado, df_ohe], axis=1)

    # Normaliza colunas numéricas
    from sklearn.preprocessing import MinMaxScaler, PowerTransformer, StandardScaler
    escalador_minmax = MinMaxScaler(feature_range=(0, 1))
    df_processado[['tenure', 'MonthlyCharges_escalado']] = escalador_minmax.fit_transform(df[['tenure', 'MonthlyCharges']])
    transformador_potencia = PowerTransformer(method='yeo-johnson')
    total_charges_transformado = transformador_potencia.fit_transform(df[[coluna_para_transformar]])
    padronizador = StandardScaler()
    total_charges_padronizado = padronizador.fit_transform(total_charges_transformado)
    df_processado['TotalCharges_padronizado'] = total_charges_padronizado

    # Adiciona a coluna SeniorCitizen e a variável alvo
    df_processado['SeniorCitizen'] = df['SeniorCitizen']
    df_processado[coluna_alvo] = df[coluna_alvo].map({'Yes': 1, 'No': 0})
    
    # --- 3. Salva o DataFrame processado ---
    # Garante que o diretório de saída exista antes de salvar
    output_dir = os.path.dirname(output_path)
    if output_dir: # Só cria se o caminho não for vazio
        os.makedirs(output_dir, exist_ok=True)
        
    df_processado.to_csv(output_path, index=False)
    print(f"Dados processados salvos com sucesso em: {output_path}")

# --- Ponto de Entrada do Script ---
if __name__ == "__main__":
    # Configura o parser de argumentos de linha de comando
    parser = argparse.ArgumentParser(description="Script para pré-processamento de dados de churn.")
    
    parser.add_argument(
        "--input_path",
        type=str,
        # CORREÇÃO FINAL: Apontando para a subpasta 01_raw, como você sugeriu.
        default=os.path.join('..', 'data', '01_raw', 'telco_customer_churn.csv'), 
        help="Caminho para o arquivo CSV de dados brutos de entrada."
    )
    
    parser.add_argument(
        "--output_path",
        type=str,
        default=os.path.join('..', 'data', '02_processed', 'telco_customer_churn_processed.csv'), 
        help="Caminho para salvar o arquivo CSV de dados processados."
    )
    
    args = parser.parse_args()

    # Executa a função principal com os argumentos fornecidos (seja pelo terminal ou os padrões)
    preprocess_data(args.input_path, args.output_path)