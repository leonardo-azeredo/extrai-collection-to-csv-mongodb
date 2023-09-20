from bson.json_util import dumps
from pymongo import MongoClient
import csv
import pandas as pd
from flask import Flask, render_template, request, send_file, redirect, url_for

app = Flask(__name__)

# Variáveis para configurar a conexão e a coleção
MONGODB_HOST = "1"
MONGODB_PORT = 27017
MONGODB_USERNAME = ""
MONGODB_PASSWORD = ""
MONGODB_DB_NAME = ""
MONGODB_COLLECTION_NAME = ""

# Senha para autenticação simples
PASSWORD = "itaventures@2023WA"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Obter a senha inserida pelo usuário
        password = request.form.get("password")

        # Verificar se a senha está correta
        if password == PASSWORD:
            # Obter o nome da coleção do campo de entrada de texto
            collection_name = request.form.get("collection_name")

            # Conexão com o banco de dados
            client = MongoClient(
                f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DB_NAME}?retryWrites=true&connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-1"
            )
            db = client[MONGODB_DB_NAME]

            # Verificar se a coleção existe
            if collection_name in db.list_collection_names():
                collection = db[collection_name].find({})

                # Converter a coleção diretamente para CSV
                df = pd.DataFrame(list(collection))
                csv_filename = f"{collection_name}.csv"
                df.to_csv(csv_filename, index=False)

                return send_file(
                    csv_filename,
                    as_attachment=True,
                    download_name=csv_filename,
                    mimetype="text/csv",
                )
            else:
                return "A coleção especificada não existe."
        else:
            return "Senha incorreta. Por favor, tente novamente."

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
