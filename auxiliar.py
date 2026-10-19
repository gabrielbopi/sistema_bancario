import os
clear = 'cls' if os.name == 'nt' else 'clear'
os.system(clear)

def cadastra_endereco():
    os.system(clear)
    print("Agora vamos cadastrar seu endereço.")
    logradouro = ""
    while logradouro=="":
        logradouro = input('Escreva o logradouro: ')

    numero = ""
    while numero=="":
        numero = input('Escreva o numero: ')
        if not numero.isdigit():
            print('Escreva apenas números!')
            numero = ""

    bairro = ""
    while bairro=="":
        bairro = input('Escreva o bairro: ')

    cidade = ""
    while cidade=="":
        cidade = input('Escreva a cidade: ')

    ufs = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
    estado = ""
    while estado=="":
        estado = input('Escreva a sigla do estado (Ex: BA, SP, ...): ')
        if estado.upper() not in ufs:
            print('Estado no formato incorreto!')
            estado = ""
    return f"{logradouro}, {numero} - {bairro} - {cidade}/{estado.upper()}"


def cria_usuario():
    nome = ""
    while nome=="":
        nome = input('Escreva o nome: ')
        contem_numero = any(char.isdigit() for char in nome)
        if contem_numero:
            print('O nome não pode conter números!')
            nome = ""

    data = ""
    while data=="":
        data = input('Escreva a sua data de nascimento (formato DD/MM/AAAA): ')
        if len(data)!=10: #Verifica tamanho do campo
            print('Formato inválido. A data deve ter a quantidade especificada de dígitos!') 
            data = ""
        elif not (data[2]=='/' and data[5]=='/'): #Verifica se há barras
            print('Formato inválido. Não esqueça as barras (/)!') 
            data = ""
        elif not all(char.isdigit() for char in data.replace('/','')): #Verifica se os digitos são numéricos
            print('Escreva apenas números e barras de acordo com o formato especificado!')
            data = ""
        elif int(data[:2])>31 or int(data[3:5])>12 or int(data[6:10])>2026 :
            print('Valor invalido para o dia, mês ou ano!')
            data = ""

    cpf = ""
    while cpf=="":
        cpf = input('Escreva seu CPF (apenas números): ')
        if len(cpf)!=11: #Verifica tamanho do campo
            print('Formato inválido. O CPF deve conter 11 dígitos!') 
            cpf = ""
        elif not all(char.isdigit() for char in cpf): #Verifica se os digitos são numéricos
            print('Escreva apenas números de acordo com o formato especificado para o CPF!')
            cpf = ""
    
    os.system(clear)
    return dict(nome=nome.title(), data=data, cpf=cpf, endereco=cadastra_endereco())

print(cria_usuario())