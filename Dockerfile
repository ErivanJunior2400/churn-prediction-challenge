FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Se o requirements.txt não mudar, o Docker não reinstala tudo de novo.
COPY requirements.txt .

# Adicionamos 'jupyterlab' aqui para garantir que ele esteja na lista.
RUN pip install --no-cache-dir -r requirements.txt && pip install jupyterlab

# Copia TODOS os outros arquivos do projeto para o diretório de trabalho do container
COPY . .

# Expõe a porta 8888, que é a porta padrão do Jupyter
EXPOSE 8888

# O comando que será executado quando o container iniciar.
# Inicia o Jupyter Lab de forma que ele seja acessível externamente.
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--IdentityProvider.password='desafio'"]
