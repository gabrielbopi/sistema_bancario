import os
clear = 'cls' if os.name == 'nt' else 'clear'
os.system(clear)

def cadastrar_endereco():
    os.system(clear)
    print("Agora vamos cadastrar seu endereço.")
    logradouro = ""
    while logradouro=="":
        logradouro = input('Escreva o logradouro: ')

    numero = ""
    while numero=="":
        input_numero = input('Escreva o numero: ')
        if not input_numero.isdigit():
            print('Escreva apenas números!')
        else:
            numero = input_numero
    bairro = ""
    while bairro=="":
        bairro = input('Escreva o bairro: ')

    cidade = ""
    while cidade=="":
        cidade = input('Escreva a cidade: ')

    ufs = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
    estado = ""
    while estado=="":
        input_estado = input('Escreva a sigla do estado (Ex: BA, SP, ...): ')
        if input_estado.upper() not in ufs:
            print('Estado no formato incorreto!')
        else:
            estado = input_estado.upper()

    os.system(clear)
    return f"{logradouro}, {numero} - {bairro} - {cidade}/{estado}"



def criar_usuario(usuario):
    nome = ""
    while nome=="":
        input_nome = input('Escreva o nome: ')
        contem_numero = any(char.isdigit() for char in input_nome)
        if contem_numero:
            print('O nome não pode conter números!')
        else:
            nome = input_nome
    data = ""
    while data=="":
        input_data = input('Escreva a sua data de nascimento (formato DD/MM/AAAA): ')
        if len(input_data)!=10: #Verifica tamanho do campo
            print('Formato inválido. A data deve ter a quantidade especificada de dígitos!') 
        elif not (input_data[2]=='/' and input_data[5]=='/'): #Verifica se há barras
            print('Formato inválido. Não esqueça as barras (/)!') 
        elif not all(char.isdigit() for char in input_data.replace('/','')): #Verifica se os digitos são numéricos
            print('Escreva apenas números e barras de acordo com o formato especificado!')
        elif int(input_data[:2])>31 or int(input_data[3:5])>12 or int(input_data[6:10])>2026 :
            print('Valor invalido para o dia, mês ou ano!')
        else:
            data = input_data

    cpf = ""
    while cpf=="":
        input_cpf = input('Escreva seu CPF (apenas números): ')
        if len(input_cpf)!=11: #Verifica tamanho do campo
            print('Formato inválido. O CPF deve conter 11 dígitos!') 
        elif not all(char.isdigit() for char in input_cpf): #Verifica se os digitos são numéricos
            print('Escreva apenas números de acordo com o formato especificado para o CPF!')
        elif any([individuo['cpf']==input_cpf for individuo in usuario]): #Verifica se já existe esse CPF já cadastrado para outros usuários
            print('Não foi possível cadastrar. Uma pessoa com esse CPF já existe no sistema!')
        else:
            cpf = input_cpf 
    usuario.append(dict(nome=nome.title(), data=data, cpf=cpf, endereco=cadastrar_endereco()))
    os.system(clear)
    print(f'Criado usuário: {usuario}')
    
    return usuario

def criar_conta(conta, usuario):
    agencia = '0001'
    if len(conta)==0:
        numero = 1
    else:
        numero = conta[-1]['numero'] + 1
    conta.append(dict(agencia=agencia, numero=numero, usuario=usuario['cpf']))
    os.system(clear)
    print(f'''Conta associada ao usuário {usuario['nome']}:
        Agencia: {conta[-1]['agencia']}, número: {conta[-1]['numero']}''')

    return conta

usuario = []; conta = []
usuario.append(dict(nome='alguem1', data='01', cpf='01234567890', endereco=''))
usuario.append(dict(nome='alguem2', data='02', cpf='01234567891', endereco=''))
i=-1
conta0 = dict(agencia = '0001', numero=1, usuario=usuario[i])
conta.append(conta0)
# usuario = criar_usuario(usuario)
conta = criar_conta(conta, usuario[i])


# print(conta)

# print(usuario)
# print(conta)