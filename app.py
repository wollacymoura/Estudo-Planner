from flask import Flask, render_template, request
import EstudoPlanner

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    resultado = None
    erro = None
    if request.method == 'POST':
        try:
            # Recebe tempos disponíveis por dia
            for dia in EstudoPlanner.dias_da_semana.keys():
                EstudoPlanner.dias_da_semana[dia] = int(request.form.get(dia, 0))

            # Limpa matérias antigas
            EstudoPlanner.materias.clear()

            # Recebe matérias e pesos
            i = 1
            while True:
                nome = request.form.get(f'materia_nome_{i}')
                peso = request.form.get(f'materia_peso_{i}')
                if nome and peso:
                    EstudoPlanner.materias[nome] = {"peso": int(peso)}
                    i += 1
                else:
                    break

            # Processa dados
            EstudoPlanner.formatacao_de_dados()
            distribuicao = EstudoPlanner.distribuicao_por_dia()

            # Gera o PDF com a rotina de estudos
            EstudoPlanner.gerar_pdf(distribuicao)
            resultado = "O PDF com a rotina de estudos foi gerado com sucesso!"
        except Exception as e:
            erro = str(e)

    return render_template("home.html", resultado=resultado, erro=erro)


if __name__ == '__main__':
    app.run(debug=True)
