from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd

# Carregar o modelo treinado
modelo = joblib.load("melhor_pipeline.pkl")

# Inicializar o app Flask
app = Flask(__name__)

# Página inicial
@app.route('/')
def index():
    return render_template('form.html')

# Rota para processar a previsão
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Coletar os dados do formulário
        sexo = request.form['sexo']  # Masculino ou Feminino
        dependentes = int(request.form['dependentes'])  # Número de dependentes
        casado = request.form['casado']  # Sim ou Não
        autonomo = request.form['autonomo']  # Sim ou Não
        rendimento = float(request.form['rendimento'])  # Rendimento mensal
        educacao = request.form['educacao']  # Educação
        valoremprestimo = float(request.form['valoremprestimo'])  # Valor do empréstimo

        if dependentes == "3 ou mais":
            dependentes = 3
        else:
            dependentes = int(dependentes)

        # Pré-processamento das variáveis (exemplo, ajuste conforme necessário)
        sexo_bin = 1 if sexo == 'M' else 0
        casado_bin = 1 if casado == 'Sim' else 0
        autonomo_bin = 1 if autonomo == 'Sim' else 0
        educacao_bin = 1 if educacao == 'Graduado' else 0  # Exemplo de codificação

        # Criando DataFrame
        d = {'Gender': [sexo_bin], 'Married': [casado_bin], 'Dependents': [dependentes],
             'Education': [educacao_bin], 'Self_Employed': [autonomo_bin], 'ApplicantIncome': [valoremprestimo], 'LoanAmount': [rendimento]}
    
        data = pd.DataFrame(data=d)

        # Fazer a previsão
        previsao = modelo.predict(data)

        # Retornar o resultado
        resultado = "Aprovado" if previsao[0] == 1 else "Negado"
        return render_template('response.html', result=resultado)

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
