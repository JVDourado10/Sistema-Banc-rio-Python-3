from datetime import datetime
from abc import ABC, abstractclassmethod, abstractproperty

class Conta: 
  def __init__(self, numero, cliente):
    self._saldo = 0
    self._numero = numero
    self._agencia = "0001"
    self._cliente = cliente
    self._historico = Historico()

  @property
  def saldo(self):
    return self._saldo

  @classmethod
  def nova_conta(cls, numero, cliente):
    return cls(numero, cliente)

  def sacar(self, valor):
    if valor <= 0:
      print("Operração Falhou, você digitou um valor inválido")
      return False
    elif valor > self._saldo:
      print('Operação Falhou! Saldo Insuficiente')
      return False
    else:
      print('Saque Realizado com Sucesso')
      print(f"Saque de R$ {valor:.2f} realizado com sucesso \n\nSaldo Anterior: {self.saldo}")
      self._saldo -= valor
      print(f"Novo Saldo: {self._saldo}")
      return True
    
  def depositar(self, valor):
    if valor > 0:
      print(f"Depósito de R$ {valor:.2f} feito com sucesso \n\nSaldo Anterior: {self._saldo}")
      self._saldo += valor
      print(f"Novo Saldo: {self._saldo}")
      return True
    else:
      print("Valor Inválido")
      return False
    
class ContaCorrente(Conta):
  def __init__(self, numero, cliente, limite=500, limite_saques=3):
    super().__init__(numero, cliente)
    self.limite = limite
    self.limite_saques = limite_saques

  def sacar(self, valor):
    numero_saques = len(
      [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
    )

    if valor > self.limite:
      print(f"Operação falhou! O saque não pode exceder o seu limite de R$ {self.limite:.2f}")

    elif numero_saques >= self.limite_saques:
      print(f"Operação falhou! Você já atingiu o seu limite de {self.limite_saques} saques diários")

    else:
      return super().sacar(valor)

    return False
  
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

class Historico:
  def __init__(self):
    self._transacoes = []

  @property
  def transacoes(self):
    return self._transacoes

  def adicionar_transacao(self, transacao):
    self._transacoes.append(
      {
        "tipo": transacao.__class__.__name__,
        "valor": transacao.valor,
        "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
      }
    )

class Transacao(ABC):
  @property
  @abstractproperty
  def valor(self):
    pass
  
  @abstractclassmethod
  def registrar(self, conta):
    pass

class Saque(Transacao):
  def __init__(self, valor):
    self._valor = valor

  @property
  def valor(self):
    return self._valor
  
  def registrar(self, conta):
    if conta.sacar(self.valor):
      conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
  def __init__(self, valor):
    self._valor = valor

  @property
  def valor(self):
    return self._valor

  def registrar(self, conta):
    if conta.depositar(self.valor):
        conta.historico.adicionar_transacao(self)