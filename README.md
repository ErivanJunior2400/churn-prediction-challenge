<!-- Badges -->
<p align="center">
<img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python" alt="Python Version">
<img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow?style=for-the-badge" alt="Project Status">
<img src="https://img.shields.io/badge/Tests-Passing-brightgreen?style=for-the-badge&logo=githubactions" alt="Tests Status">
<img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

<h1 align="center">Análise e Previsão de Churn para Empresa de Telecomunicações</h1>

📝 Descrição do Projeto
Este projeto consiste em uma solução de ponta a ponta para o problema de rotatividade de clientes (churn) em uma empresa de telecomunicações. O objetivo é analisar um conjunto de dados para descobrir os principais fatores que levam ao cancelamento de serviços e, a partir desses insights, construir e avaliar um modelo de machine learning capaz de prever quais clientes estão em risco.

O trabalho abrange desde a limpeza e análise exploratória dos dados até o treinamento, comparação de modelos, interpretação de resultados e a criação de um pipeline automatizado, visando entregar uma solução robusta, reprodutível e com insights acionáveis para a área de negócios.

## 📂 Estrutura de Pastas

O repositório está organizado da seguinte forma para garantir clareza, modularidade e reprodutibilidade:

```text
churn-prediction-challenge/
|
|-- data/
|   |-- 01_raw/                 # Dados originais e imutáveis
|   |-- 02_processed/           # Dados intermediários após limpeza
|   |-- 03_output/              # Arquivos finais gerados (ex: previsões)
|
|-- notebooks/
|   |-- 01_EDA.ipynb            # Notebook para Análise Exploratória de Dados
|   |-- 02_Modeling.ipynb       # Notebook para experimentação e comparação de modelos
|
|-- src/
|   |-- data_preprocessing.py   # Script para pré-processamento dos dados
|   |-- train_model.py          # Script para treinamento do modelo
|   |-- evaluate_model.py       # Script para avaliação do modelo
|
|-- reports/
|   |-- Decision_Log.md         # Log com justificativas das decisões técnicas
|
|-- tests/
|   |-- __init__.py
|   |-- test_data_processing.py # Testes para o pré-processamento
|
|-- .github/workflows/
|   |-- pipeline.yml            # Define a pipeline de automação (CI/CD)
|
|-- .gitignore                  # Arquivos e pastas ignorados pelo Git
|-- Dockerfile                  # Receita para criar o ambiente em um container
|-- Makefile                    # Comandos para automatizar o pipeline (make train, etc.)
|-- README.md                   # Documentação principal (este arquivo)
|-- requirements.txt            # Lista de dependências Python
```

🚀 Instalação e Execução
Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

Pré-requisitos
`Git`

`Python` (versão 3.9 ou superior)

Passo a Passo para Instalação
Clone o repositório:

`git clone https://github.com/ErivanJunior2400 churn-prediction-challenge.git`
`cd churn-prediction-challenge`

Crie e ative um ambiente virtual:

# Cria o ambiente
`python -m venv venv`

# Ativa o ambiente no Windows
`.\venv\Scripts\activate`
# (Alternativa para macOS/Linux)
`source venv/bin/activate`

Instale as dependências:

`pip install -r requirements.txt`

⚡ Exemplo de Execução
Após a instalação, a análise completa e o treinamento do modelo podem ser executados através do Jupyter Notebook principal.

Inicie o Jupyter Lab:

`jupyter lab`
Execute o Notebook:

No menu à esquerda do Jupyter Lab, navegue até a pasta /notebooks.

Abra o notebook principal (ex: 1.0-analise-e-modelagem.ipynb).

Para executar todo o processo, vá ao menu superior e clique em Kernel > Restart Kernel and Run All Cells....

✅ Testes Automatizados
Para garantir a qualidade e a confiabilidade das funções de pré-processamento, foram implementados testes unitários utilizando a biblioteca pytest.

Executando os Testes
Com o ambiente virtual ativado, você pode rodar todos os testes automatizados com um único comando na raiz do projeto:

`pytest`

Isso descobrirá e executará automaticamente todos os testes localizados na pasta /tests.

Nota sobre Badges: Os badges de Build e Cobertura de Testes no topo deste README são exemplos de como um projeto com Integração Contínua (CI/CD) via GitHub Actions se apresentaria. Eles refletem a intenção de seguir as melhores práticas, mesmo que a pipeline de CI completa não seja o foco deste desafio.