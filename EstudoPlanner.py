from fpdf import FPDF

# Dicionário para armazenar os minutos disponíveis por dia da semana
dias_da_semana = {
    "segunda": None,
    "terça": None,
    "quarta": None,
    "quinta": None,
    "sexta": None,
    "sábado": None,
    "domingo": None
}

# Dicionário para armazenar matérias, cada uma com peso e tempo de estudo
materias = {}

# Função que coleta dados do usuário sobre tempo disponível e matérias
def entrada_de_dados():
    print("Informe quantos minutos você tem disponíveis por dia para estudar:")
    for dia in dias_da_semana:
        while True:
            try:
                tempo = int(input(f"{dia.capitalize()}: "))
                dias_da_semana[dia] = tempo
                break
            except ValueError:
                print("Por favor, insira um número inteiro válido.")

    while True:
        try:
            qtd_materias = int(input("\nQuantas matérias você deseja cadastrar? "))
            break
        except ValueError:
            print("Por favor, insira um número inteiro válido.")

    for i in range(qtd_materias):
        nome = input(f"\nNome da {i+1}ª matéria: ")
        while True:
            try:
                peso = int(input(f"Peso (1 a 4) para {nome}: "))
                if 1 <= peso <= 4:
                    break
                else:
                    print("O peso deve ser entre 1 e 4.")
            except ValueError:
                print("Por favor, insira um número inteiro válido.")
        materias[nome] = {"peso": peso}

# Função que calcula o tempo ideal de estudo para cada matéria com base nos pesos
def formatacao_de_dados():
    tempo_total = sum(dias_da_semana.values())  # Soma total de tempo disponível na semana
    peso_total = sum(materia["peso"] for materia in materias.values())  # Soma total dos pesos
    tempo_medio_por_peso = tempo_total / peso_total  # Quanto vale cada ponto de peso em minutos

    tempo_acumulado = 0
    materias_lista = list(materias.items())

    for i, (nome, dados) in enumerate(materias_lista):
        peso = dados["peso"]
        if i == len(materias_lista) - 1:
            tempo = tempo_total - tempo_acumulado  # Garante que o tempo total será 100% utilizado
        else:
            tempo = round(peso * tempo_medio_por_peso)
            tempo_acumulado += tempo

        materias[nome]["tempo"] = tempo  # Armazena o tempo ideal para a matéria

# Função que distribui o tempo de cada matéria entre os dias da semana proporcionalmente
def distribuicao_por_dia():
    distribuicao_local = {}
    for dia in dias_da_semana:
        distribuicao_local[dia] = {}  # Inicializa cada dia com um dicionário vazio

    tempo_total = sum(dias_da_semana.values())

    # Para cada matéria, divide seu tempo entre os dias da semana de forma proporcional
    for materia, dados in materias.items():
        tempo_materia = dados["tempo"]
        tempo_acumulado = 0
        dias = list(dias_da_semana.items())

        for i, (dia, tempo_dia) in enumerate(dias):
            if i == len(dias) - 1:
                tempo_para_materia = tempo_materia - tempo_acumulado  # Garante soma exata
            else:
                proporcao = tempo_dia / tempo_total
                tempo_para_materia = round(tempo_materia * proporcao)
                tempo_acumulado += tempo_para_materia

            distribuicao_local[dia][materia] = tempo_para_materia

    # Ajusta possíveis diferenças por arredondamento garantindo que o tempo por dia seja 100%
    for dia, tempo_disponivel in dias_da_semana.items():
        soma = sum(distribuicao_local[dia].values())
        diferenca = tempo_disponivel - soma
        if diferenca != 0:
            ultima_materia = list(distribuicao_local[dia].keys())[-1]
            distribuicao_local[dia][ultima_materia] += diferenca

    return distribuicao_local

# Função que cria um PDF com a rotina de estudos


def gerar_pdf(distribuicao_local):
    # Usa orientação paisagem (landscape)
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Rotina de Estudos', ln=True, align='C')
    pdf.ln(10)

    # Calcula largura das células para preencher a página
    num_colunas = len(dias_da_semana) + 1  # +1 para coluna "Matéria"
    page_width = pdf.w - 2 * pdf.l_margin
    cell_width = page_width / num_colunas
    cell_height = 10

    # Cabeçalho da tabela
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(cell_width, cell_height, "Matéria", border=1, align='C')
    for dia in dias_da_semana:
        pdf.cell(cell_width, cell_height, dia.capitalize(), border=1, align='C')
    pdf.ln(cell_height)

    # Linhas da tabela: uma para cada matéria
    pdf.set_font('Arial', '', 10)
    for materia in materias:
        pdf.cell(cell_width, cell_height, materia, border=1, align='C')
        for dia in dias_da_semana:
            tempo = distribuicao_local[dia][materia]
            pdf.cell(cell_width, cell_height, f"{tempo} min", border=1, align='C')
        pdf.ln(cell_height)

    pdf.output('rotina_de_estudos.pdf')
    print("\nO PDF com a rotina de estudos foi gerado com sucesso!")

# Função que cria um arquivo .txt com a rotina de estudos


def gerar_txt(distribuicao_local):
    # Criação do arquivo .txt
    with open("rotina_de_estudos.txt", "w") as file:
        file.write("Rotina de Estudos\n")
        file.write("=" * 30 + "\n")
        
        # Percorrendo cada dia da semana e suas matérias
        for dia, materias_dia in distribuicao_local.items():
            file.write(f"\n{dia.capitalize()}:\n")
            for materia, tempo in materias_dia.items():
                file.write(f"  - {materia}: {tempo} min\n")
            file.write("\n")  # Espaço entre os dias
    
    print("\nO arquivo de texto com a rotina de estudos foi gerado com sucesso!")

# Execução do programa
entrada_de_dados()
formatacao_de_dados()
distribuicao_local = distribuicao_por_dia()

# Gerar o PDF
gerar_pdf(distribuicao_local)

# Gerar o arquivo de texto
gerar_txt(distribuicao_local)