import os
clear = 'cls' if os.name == 'nt' else 'clear'
os.system(clear)

#FUNÇÕES
#Cadastro:
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

def criar_conta(conta, usuarios):
    idx_usuario = procurar_usuario(usuarios)
    usuario = usuarios[idx_usuario]
    agencia = '0001'
    if len(conta)==0:
        numero = 1
    else:
        numero = str(int(conta[-1]['numero']) + 1) #Atribui à atual um número que é o sucessor do da ultima conta cadastrada.
    conta.append(dict(agencia=agencia, numero=numero, saldo = 0, limite = 500, extrato = "", numero_saques = 0,usuario=usuario))
    os.system(clear)
    print(f'''Conta associada ao usuário {usuario['nome']}:
        Agencia: {conta[-1]['agencia']}, número: {conta[-1]['numero']}''')

    return conta

#Para procura:
def procurar_usuario(usuario):
    os.system(clear)
    cpf = ""
    while cpf=="":
        input_cpf = input('Escreva o CPF do usuário para a conta (apenas números): ')
        if len(input_cpf)!=11: #Verifica tamanho do campo
            print('Formato inválido. O CPF deve conter 11 dígitos!') 
        elif not all(char.isdigit() for char in input_cpf): #Verifica se os digitos são numéricos
            print('Escreva apenas números de acordo com o formato especificado para o CPF!')
        elif not any([individuo['cpf']==input_cpf for individuo in usuario]): #Verifica se já existe esse CPF já cadastrado para outros usuários
            print('CPF não encontrado no sistema! Digite um usuário já cadastrado.')
        else:
            cpf = input_cpf
            idx_usuario = [individuo['cpf'] for individuo in usuario].index(cpf)

    return idx_usuario
            
def procurar_conta(contas):
    os.system(clear)
    numero = 0
    while numero == 0:
        input_numero = input('Escreva o número da conta (apenas números): ')
        
        if not all(char.isdigit() for char in input_numero): #Verifica se os digitos são numéricos
            print('Escreva apenas digitos numéricos!')
        elif not any([conta['numero']==input_numero for conta in contas]): #Verifica se o número existe
            print('Número não encontrado no sistema! Digite uma conta já cadastrada.')
        else:
            numero = input_numero
            idx_conta = [conta['numero'] for conta in contas].index(numero)

    return idx_conta

# Para cada conta:
def depositar(saldo,extrato,/):
    os.system(clear)

    valor = ''
    while True:
        input_valor = input("Informe o valor do depósito: ")
        if not input_valor.isdigit(): #Verifica se os digitos são numéricos
            print('Escreva apenas digitos numéricos!')
        else:
            valor = float(input_valor)
            break

    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"

    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo,extrato

def sacar(*,saldo,extrato, n_saques, limite):
    global LIMITE_SAQUES

    os.system(clear)
    valor = ''
    while True:
        input_valor = input("Informe o valor do saque: ")
        if not input_valor.isdigit(): #Verifica se os digitos são numéricos
            print('Escreva apenas digitos numéricos!')
        else:
            valor = float(input_valor)
            break

    excedeu_saldo = valor > saldo

    excedeu_limite = valor > limite

    excedeu_saques = n_saques >= LIMITE_SAQUES

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        n_saques += 1

    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo,extrato,n_saques

def mostrar_extrato(saldo, /, *, extrato):
    os.system(clear)
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

#Menus:
def opcoes_conta(conta):
    menu = """
    Escolha a operação para a conta:

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair

    => """

    while True:
        saldo = conta['saldo']; extrato = conta['extrato']
        numero_saques = conta['numero_saques']; limite = conta['limite']
        opcao = input(menu)

        if opcao == "d":
            conta['saldo'],conta['extrato'] = depositar(saldo,extrato)

        elif opcao == "s":
            conta['saldo'],conta['extrato'],conta['numero_saques']= sacar(saldo=saldo, extrato=extrato, n_saques=numero_saques, limite=limite)
            
        elif opcao == "e":
            mostrar_extrato(saldo,extrato=extrato)

        elif opcao == "q":
            return conta

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


def menu_principal(usuarios, contas):
    os.system(clear)
    
    menu = """
    Bem vindo ao internet banking! Tecle uma opção:

    [u] cadastrar usuário
    [c] cadastrar conta
    [a] acessar conta
    [q] Sair

    => """

    while True:

        opcao = input(menu)

        match opcao:
            case 'u':
                usuarios = criar_usuario(usuarios)
            case 'c':
                contas = criar_conta(contas, usuarios)
            case 'a':
                idx_conta = procurar_conta(contas)
                conta = contas[idx_conta]
                os.system(clear)
                print(f'''Conta associada ao usuário {conta['usuario']['nome']}
                        Agencia: {conta['agencia']}, número: {conta['numero']}''')
                contas[idx_conta] = opcoes_conta(conta)
                
            case 'q':
                break
            case _:
                print("Operação inválida, por favor selecione novamente a operação desejada.")





#CORPO DO PROGRAMA

LIMITE_SAQUES = 3
usuarios = []; contas = []


menu_principal(usuarios, contas)
