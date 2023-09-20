# Use uma imagem base Python
FROM python:3.8

# Crie um diretório de trabalho no container
WORKDIR /app

# Copie os arquivos Python para o diretório de trabalho
COPY . .

# Instale as dependências Python
RUN pip install -r requirements.txt  # Se você tiver um arquivo requirements.txt

# Exponha a porta em que o aplicativo Flask está ouvindo (padrão 5000)
EXPOSE 5000

# Defina a variável de ambiente para o Flask
ENV FLASK_APP=app.py

# Comando para executar o aplicativo Flask
CMD ["flask", "run", "--host", "0.0.0.0"]
