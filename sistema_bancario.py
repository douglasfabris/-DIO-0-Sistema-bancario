from abc import ABC, abstractproperty, abstractclassmethod

class Cliente:
    def __init__(self, endereco):
      self.endereco = endereco
      self.contas = []

    def realizar_transacao(self, conta, transacao):
       transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
       self.contas.append

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
       super().__init__.endereco
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
      return cls(cliente, numero)
   
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
      self.limite = limite
      self.limite_saques = limite_saques

    def sacar(self, valor):
      numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"]==Saque.__name__])

      excedeu_limite = valor > self.limite
      excedeu_saques = numero_saques > self.limite_saques

      if excedeu_limite:
         print("Excedeu o valor limite de saques")

      elif excedeu_saques:
         print("Excedeu o número limite de saques")
    
      else:
         return super().sacar(valor)
      
      return False

    def __str__(self):
       return f"""
            Agência: ${self.agencia}
            Conta: ${self.numero}
            Titular: ${self.cliente.nome}"""

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
         "data": "10/10/2020"
      })

class Transacao(ABC):
   @property
   @abstractproperty
   def value(self):
      pass
   @abstractclassmethod
   def registrar(self):
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

def exibir_extrato(saldo, /, *, extrato):
  print("\n================ EXTRATO ================")
  print("Não foram realizadas movimentações." if not extrato else extrato)
  print(f"\nSaldo: R$ {saldo:.2f}")
  print("==========================================")

def criar_usuario(usuarios):
   cpf = input("Digite o CPF do novo usuario: ")
   usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"]==cpf]
   if usuarios_filtrados:
      print("Usuário já cadastrado")
      return
   nome = input("Digite o nome: ")
   data_nascimento = input("Digite a data de nascimento: ")
   endereco = input("Digite o endereco: ")

   usuarios.append({"cpf": cpf, "nome": nome, "data de nascimento": data_nascimento, "endereco": endereco})
   print("Usuário criado com sucesso")

def criar_conta(usuarios, agencia, conta):
   cpf = input("Digite o CPF do usuario: ")
   usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"]==cpf]
   if (not usuarios_filtrados):
      print("usuario não encontrado")
      return
   print("conta criada com sucesso")
   return {"agencia": agencia, "conta": conta, "usuario": usuarios_filtrados[0]}

def listar_contas(contas):
   for conta in contas:
      print(f"""
        Conta:{conta["conta"]}
        Agência: {conta["agencia"]}
        Titular: {conta["usuario"]["nome"]}
        """)
      
def main():
  saldo = 0
  limite = 500
  extrato = ""
  numero_saques = 0
  LIMITE_SAQUES = 3
  usuarios = []
  contas = []
  agencia = "0001"
  while True:
      opcao = menu()
      if opcao == "d":
          valor = float(input("Informe o valor do depósito: "))
          saldo, extrato = depositar(saldo, valor, extrato)

      elif opcao == "s":
          valor = float(input("Informe o valor do saque: "))
          saldo, extrato = sacar(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)

      elif opcao == "e":
        exibir_extrato(saldo, extrato=extrato)
      
      elif opcao == "c":
         criar_usuario(usuarios)
      
      elif opcao == "cc":
         numero_conta = len(contas) + 1
         conta = criar_conta(usuarios, agencia, numero_conta)
         if conta:
            contas.append(conta)
      
      elif opcao == "lc":
         listar_contas(contas)

      elif opcao == "q":
          break

      else:
          print("Operação inválida, por favor selecione novamente a operação desejada.")

main()