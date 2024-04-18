from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

class Cliente:
    def __init__(self, endereco):
      self.endereco = endereco
      self.contas = []

    def realizar_transacao(self, conta, transacao):
       transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
       self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
       super().__init__(endereco)
       self.nome = nome
       self.data_nascimento = data_nascimento
       self.cpf = cpf

class Conta:
   def __init__(self, numero, cliente):
      self._saldo = 0
      self._numero = numero
      self._agencia = "0001"
      self._cliente = cliente
      self._historico = Historico()

   @classmethod
   def nova_conta(cls, cliente, numero):
      return cls(numero, cliente)
   
   @property
   def saldo(self):
      return self._saldo
   
   @property
   def numero(self):
      return self._numero
   
   @property
   def agencia(self):
      return self._agencia
   
   @property
   def cliente(self):
      return self._cliente
   
   @property
   def historico(self):
      return self._historico
   
   def sacar(self, valor):
        saldo = self.saldo
        if (valor>saldo):
            print("Você não tem saldo suficiente")
        elif valor > 0:
            self._saldo -= valor
            return True
        else:
            print("Operação falhou! O valor informado é inválido.")
        
        return False

   def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso")
        else:
            print("Digite um número válido")
            return False
        return True
   
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
      super().__init__(numero, cliente)
      self._limite = limite
      self._limite_saques = limite_saques

    def sacar(self, valor):
      numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"]==Saque.__name__])

      excedeu_limite = valor > self._limite
      excedeu_saques = numero_saques > self._limite_saques

      if excedeu_limite:
         print("Excedeu o valor limite de saques")

      elif excedeu_saques:
         print("Excedeu o número limite de saques")
    
      else:
         return super().sacar(valor)
      
      return False

    def __str__(self):
       return f"""\
            Agência: {self.agencia}
            Conta: {self.numero}
            Titular: {self.cliente.nome}"""

class Historico:
   def __init__(self):
      self._transacoes = []

   @property
   def transacoes(self):
      return self._transacoes
   
   def adicionar_transacao(self, transacao):
      self._transacoes.append({
         "tipo": transacao.__class__.__name__,
         "valor": transacao.valor,
         "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
      })

class Transacao(ABC):
   @property
   @abstractmethod
   def valor(self):
      pass
   @classmethod
   @abstractmethod
   def registrar(self, conta):
      pass
   
class Saque(Transacao):
   def __init__(self, valor):
      self._valor = valor
    
   @property
   def valor(self):
      return self._valor
   
   def registrar(self, conta):
      sucesso_transacao = conta.sacar(self.valor)

      if sucesso_transacao:
         conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
   def __init__(self, valor):
      self._valor = valor

   @property
   def valor(self):
      return self._valor
   
   def registrar(self, conta):
      sucesso_transacao = conta.depositar(self.valor)

      if sucesso_transacao:
         conta.historico.adicionar_transacao(self)

def menu():
  menu = """

  [d] Depositar
  [s] Sacar
  [e] Extrato
  [c] Criar usuário
  [cc] Criar Conta
  [lc] Listar contas
  [q] Sair

  => """
  return input(menu)

def filtrar_clientes(cpf, clientes):
   clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
   return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
   if not cliente.contas:
      print("Cliente não possui conta")
      return
   return cliente.contas[0]

def depositar(clientes):
   cpf = input("Informe o CPF do cliente")
   cliente = filtrar_clientes(cpf, clientes)
   
   if not cliente:
      print("Cliente não encontrado")
      return
   valor = float(input("Informe o valor do depósito: "))
   transacao = Deposito(valor)
   
   conta = recuperar_conta_cliente(cliente)
   if not conta:
      return
   cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
   cpf = input("Informe o CPF do cliente")
   cliente = filtrar_clientes(cpf, clientes)
   
   if not cliente:
      print("Cliente não encontrado")
      return
   valor = float(input("Informe o valor do saque: "))
   transacao = Saque(valor)
   
   conta = recuperar_conta_cliente(cliente)
   if not conta:
      return
   cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
   cpf = input("Informe o CPF do cliente")
   cliente = filtrar_clientes(cpf, clientes)
   
   if not cliente:
      print("Cliente não encontrado")
      return

   conta = recuperar_conta_cliente(cliente)
   if not conta:
      return
   
   print("\n================ EXTRATO ================")
   transacoes = conta.historico.transacoes
   extrato = ""
   if not transacoes:
      extrato = "Não foram realizadas movimentações."
   else:
      for transacao in transacoes:
         extrato += f"\n{transacao["tipo"]}:\n\tR${transacao["valor"]:.2f}"
         
   print(extrato)
   print(f"\nSaldo: R$ {conta.saldo:.2f}")
   print("==========================================")

def criar_cliente(clientes):
   cpf = input("Digite o CPF do usuario: ")
   cliente = filtrar_clientes(cpf, clientes)
   
   if cliente:
      print("usuario ja existente")
      return
   
   nome = input("Digite o nome: ")
   data_nascimento = input("Digite a data de nascimento: ")
   endereco = input("Digite o endereco: ")

   cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
   
   clientes.append(cliente)
   
   print("Cliente criado com sucesso")

def criar_conta(numero_conta, clientes, contas):
   cpf = input("Digite o CPF do usuario: ")
   cliente = filtrar_clientes(cpf, clientes)
   
   if not cliente:
      print("usuario não encontrado")
      return
   conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
   contas.append(conta)
   cliente.contas.append(conta)
   print("conta criada com sucesso")

def listar_contas(contas):
   for conta in contas:
      print(textwrap.dedent(str(conta)))
      
def main():
  clientes = []
  contas = []
  while True:
      opcao = menu()
      if opcao == "d":
          depositar(clientes)

      elif opcao == "s":
          sacar(clientes)

      elif opcao == "e":
        exibir_extrato(clientes)
      
      elif opcao == "c":
         criar_cliente(clientes)
      
      elif opcao == "cc":
         numero_conta = len(contas) + 1
         conta = criar_conta(numero_conta, clientes, contas)
      
      elif opcao == "lc":
         listar_contas(contas)

      elif opcao == "q":
          break

      else:
          print("Operação inválida, por favor selecione novamente a operação desejada.")

main()