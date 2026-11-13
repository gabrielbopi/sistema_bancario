#Modificações feitas a partir do código original em 'https://github.com/digitalinnovationone/trilha-python-dio/blob/main/01%20-%20Estrutura%20de%20dados/desafio.py'
# Autor do novo código: Gabriel Pinheiro @gabrielbopi

from abc import ABC, abstractmethod

#CLASSES

    #Cliente
class Cliente(ABC):
    def __init__(self, endereco:str, contas:list):
        self._endereco = endereco
        self._contas = contas

    def realizar_transacao(self, conta:Conta, transacao:Transacao):
        valor = float(input("Informe o valor: "))        
        transacao(valor).registrar(conta)

    def adicionar_conta(self, conta:Conta):
        if conta:
            self._contas.append(conta)
            return True
        else:
            return False

class PessoaFisica(Cliente):
    def __init__(self, endereco:str, contas:list, cpf:str, nome:str, data_nascimento):
        super().__init__(endereco, contas)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    def __str__(self):
        return f'{self.__class__.__name__}:\n'+', '.join([f'{key.title()}={item}' for key,item in self.__dict__.items()])

    @property
    def cpf(self):
        return self._cpf

    
    #Conta
class Conta(ABC):
    _AGENCIA = "0001"
    _LIMITE_SAQUES = 3
    _VALOR_LIMITE_SAQUE = 500

    @abstractmethod
    def __init__(self, cliente:Cliente, historico:Historico, agencia:int, numero:int, saldo:float=0):
        self._cliente = cliente
        self._historico = historico
        self._agencia = agencia
        self._numero = numero
        self._saldo = saldo
        self._numero_saques = 0
     
    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def agencia(self) -> int:
        return self._agencia

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def historico(self) -> Historico:
        return self._historico

    def sacar(self, valor: float) -> bool: 
        
        excedeu_saldo = valor > self._saldo
        excedeu_limite = valor > self._VALOR_LIMITE_SAQUE
        excedeu_saques = self._numero_saques >= self._LIMITE_SAQUES

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        elif valor > 0:
            self._saldo -= valor
            self._historico.adicionar_transacao(Saque(valor))
            self._numero_saques += 1
            print("\n=== Saque realizado com sucesso! ===")

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            
            if self._saldo>=valor and valor > 0:
                self._saldo -= valor 
                return True 
            else:
                return False

    def depositar(self, valor:float) -> bool:  
        if valor > 0:
            self._saldo += valor 
            self._historico.adicionar_transacao(Deposito(valor))
            print("\n=== Depósito realizado com sucesso! ===")
            return True 
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

    @abstractmethod
    def nova_conta(cls):
        pass


class ContaCorrente(Conta):

    def __init__(self, cliente:Cliente, historico:Historico, agencia:int, numero:int, saldo:float = 0, limite:float = 2000, limite_saques:int = 3):
        super().__init__(cliente, historico, agencia, numero, saldo)
        self._limite = limite
        self._limite_saques = limite_saques

    def __str__(self):
        return f'{self.__class__.__name__}:\n'+', '.join([f'{key.title()}={item}' for key,item in self.__dict__.items()])

    @classmethod
    def nova_conta(cls, cliente, numero):  
        conta_nova = cls(cliente, Historico(), cls._AGENCIA, numero, saldo=0, limite=cls._VALOR_LIMITE_SAQUE, limite_saques=cls._LIMITE_SAQUES)
        cliente.adicionar_conta(conta_nova)
        return conta_nova

    #ITERADOR
class ContaIterador:
    def __init__(self, contas:list):
        self._contas = contas
        self._contador = 0
    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self._contas[self._contador]
            informacao = f"""\
                Agência:\t{conta._agencia}
                C/C:\t\t{conta._numero}
                Titular:\t{conta._cliente._nome}
            """
            self._contador += 1
            return informacao
        except IndexError:
            raise StopIteration
        


    #Transação
class Transacao(ABC): 
    def __init__(self, valor:float):
        self._valor = valor
  
    def __str__(self):
        return f'{self.__class__.__name__}: '+f'{self._valor}'
   
    @abstractmethod
    def registrar(self, conta:Conta):
        pass

class Deposito(Transacao):
    def registrar(self, conta:Conta):
        conta.depositar(self._valor)

class Saque(Transacao):
    def registrar(self, conta:Conta):
        conta.sacar(self._valor)

class Historico:
    def __init__(self):
        self._transacoes = []

    def __str__(self):
            return '\n'.join([f'{transacao}' for transacao in self.transacoes])
        
    def adicionar_transacao(self, transacao:Transacao):
        self.transacoes.append(transacao)

    @property
    def transacoes(self):
        return self._transacoes
    
    #GERADOR
    def gerar_relatorio(self, tipo_transacao=None):
        if tipo_transacao:
            for transacao in self._transacoes:
                yield transacao if type(transacao)==type(tipo_transacao(0)) else None
        else:
            for transacao in self._transacoes:
                yield transacao

#DECORADOR
def log_transacao(operacao):
    from datetime import datetime
    from functools import wraps
    @wraps(operacao)
    def envelope(*args, **kwargs):
        print('Transação de ' + operacao.__name__.title() + ' em ' + str(datetime.now()))
        return operacao(*args, **kwargs)    
    return envelope

#FUNÇÕES ESTÁTICAS
    #Transaçao
@log_transacao
def depositar(contas:list):
    numero_conta = int(input("Informe o número da conta (somente número):) "))
    conta = filtrar_conta(numero_conta, contas)
    if not conta:
        print("\n@@@ Conta não encontrada! @@@")
        return False
    usuario = conta.cliente
    usuario.realizar_transacao(conta, Deposito)
    return True

@log_transacao
def sacar(contas:list):
    numero_conta = int(input("Informe o número da conta (somente número):) "))
    conta = filtrar_conta(numero_conta, contas)
    if not conta:
        print("\n@@@ Conta não encontrada! @@@")
        return False
    usuario = conta.cliente
    usuario.realizar_transacao(conta, Saque)
    return True

    #Cliente
@log_transacao
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario_ocupado = filtrar_usuario(cpf, usuarios)

    if usuario_ocupado:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return usuarios

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    usuario = PessoaFisica(endereco, [], cpf, nome, data_nascimento)
    if usuario:
        usuarios.append(usuario)
        print("=== Usuário criado com sucesso! ===")
    else:
        print("\n@@@ Falha na criação do usuário! @@@")

    return usuarios

def filtrar_usuario(cpf:str, usuarios:list) -> Cliente:
    usuarios_filtrados = [usuario for usuario in usuarios if usuario.cpf == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


    #Conta
@log_transacao
def criar_conta(contas:list, usuarios:list) -> list:  
    numero = len(contas) + 1
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        conta_nova = ContaCorrente.nova_conta(usuario, numero)
        usuario.adicionar_conta(conta_nova)
        print("\n=== Conta criada com sucesso! ===")
        contas.append(conta_nova)
    else:    
        print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")

    return contas

def filtrar_conta(numero:int, contas:list) -> Conta:
    contas_filtradas = [conta for conta in contas if conta.numero == numero]
    return contas_filtradas[0] if contas_filtradas else None

def listar_contas(contas:list):
    import textwrap

    for informacao in ContaIterador(contas):
        print("=" * 100)
        print(textwrap.dedent(informacao))

@log_transacao
def exibir_extrato(contas:list):
    numero_conta = int(input("Informe o número da conta (somente número):) "))
    conta = filtrar_conta(numero_conta, contas)
    if not conta:
            print("\n@@@ Conta não encontrada! @@@")
            return False
    input_transacao = input('Qual o tipo de transacao?\n\'d\': Depósito, \'s\': Saque ou outra tecla: todos.\n')
    match input_transacao.lower():
        case 'd':
            tipo_transacao = Deposito
        case 's':
            tipo_transacao = Saque
        case _:
            tipo_transacao = None

    print("\n================ EXTRATO ================")
    extrato = ''
    for transacao in conta.historico.gerar_relatorio(tipo_transacao):
        extrato += f'{transacao}\n' if transacao else ''
    print("Não foram realizadas movimentações desse tipo." if extrato == '' else extrato)
    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")

    #Menu
def menu():
    import textwrap
    
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário (Pessoa Física)
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


#CORPO DO PROGRAMA
def main():

    usuarios = [];  contas = []

    usuario1 = PessoaFisica('algum lugar', [], '01234567890', 'alguem1', '01-02-2000')
    conta1 = ContaCorrente(usuario1, Historico(), Conta._AGENCIA, 1)
    usuario1.adicionar_conta(conta1)
    usuarios = [usuario1];  contas = [conta1]

    while True:
        opcao = menu()
        if opcao == "d":
            depositar(contas)
        
        elif opcao == "s": 
            sacar(contas)

        elif opcao == "e":
            exibir_extrato(contas)

        elif opcao == "nu": 
            usuarios = criar_usuario(usuarios)
            # print(usuarios)

        elif opcao == "nc":
            contas = criar_conta(contas, usuarios)
            print(contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()

