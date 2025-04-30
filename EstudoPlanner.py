# Armazenamento de dados

dias_da_semana = {
    "segunda": None, 
    "terça": None, 
    "quarta": None, 
    "quinta": None, 
    "sexta": None, 
    "sábado": None, 
    "domingo": None
    }

materias = {}

# Entrada de dados: quanto tempo ele tem, quais matérias ele quer estudar e qual o peso que elas tem

def entrada_de_dados():
    for dia in dias_da_semana.keys():
        minutos = input(f"Na {dia} você tem quantos minutos disponíveis para estudar? ")
        dias_da_semana[dia] = int(minutos)
    
    qntd_de_materias = int(input("quantas matérias você tem para estudar durante a semana? "))
    
    for i in range(qntd_de_materias):
        materia = input(f"Qual a {i+1}º matéria? ")
        peso = int(input(f"De (1-4), tendo em vista que 1 é o menor peso e 4 é o maior peso, Qual o peso que {materia} deve ter na sua rotina de estudos? "))
        materias[materia] = peso

entrada_de_dados()
print(dias_da_semana)
print(materias)

# formatação dos dados: ajustar o tempo de estudo na semana para a quantidade de matéria com seus respectivos pesos

def formatacao_de_dados():
    tempo_total = sum(dias_da_semana.values())
    print(tempo_total)
    

formatacao_de_dados()

# 1. Calcular o tempo total disponível na semana
# Some os minutos disponíveis de todos os dias (dias_da_semana).
# 2. Calcular o peso total das matérias
# Some todos os pesos das matérias (materias).
# 3. Calcular quanto tempo cada matéria deve receber
# Para cada matéria:
# Use a fórmula:
# tempo_da_materia = (peso_da_materia / peso_total) * tempo_total_disponível
# 4. Distribuir o tempo de cada matéria ao longo da semana