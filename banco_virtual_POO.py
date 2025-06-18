import datetime  # Necessário para registrar a data e hora das transações
import json

def salvar_dados(conta, filename="banco_dados.json"):
    """
    Salva o saldo e o extrato de uma conta em um arquivo JSON.
    """
    dados = {
        "numero_conta": conta.numero_conta, # Incluir o número da conta para recriar o objeto
        "saldo": conta.saldo,
        "extrato": conta.extrato
    }

    with open(filename, "w") as f: # Abre o arquivo "banco_dados.json" em modo de escrita ("w")
        # Salva o saldo e o extrato no arquivo usando json.dump()
        json.dump(dados, f, indent=4) # O 'indent=4' é para formatar o JSON de forma legível
    print(f"Dados da conta '{conta.numero_conta}' salvos com sucesso!")

def carregar_dados(filename="banco_dados.json"):
    """
    Carrega o saldo e o extrato de uma conta a partir de um arquivo JSON.
    """
    try:
        # Tentar abrir um arquivo chamado "banco_dados.json" em modo de leitura ("r").
        with open(filename, "r") as f:
            dados = json.load(f) # Se o arquivo existir, carregar o saldo e o extrato de lá.
            # Retorna uma nova instância de ContaBancaria com os dados carregados
            return ContaBancaria(dados["numero_conta"], dados["saldo"], dados["extrato"])
    except FileNotFoundError: # Se o arquivo não existir (FileNotFoundError), definir o saldo inicial e o extrato como uma lista vazia.
        print("Arquivo de dados não encontrado. Criando nova conta com número padrão '00000-0'.")
        return ContaBancaria("00000-0") # Retorna uma nova conta com um número padrão se o arquivo não for encontrado

class ContaBancaria:
    """Representa uma conta bancária com saldo e histórico de transações."""
    def __init__(self, numero_conta, saldo_inicial=0, extrato_inicial=None):
        self.saldo = saldo_inicial
        self.numero_conta = numero_conta
        self.extrato = extrato_inicial if extrato_inicial is not None else []

    def consultar_saldo(self):
        """Exibe o saldo atual da conta."""
        print(f"Seu saldo atual é: R$ {self.saldo:.2f}")

    def depositar(self, valor):
        """Realiza uma operação de depósito na conta."""
        try:
            valor_deposito = float(valor)
            if valor_deposito <= 0:
                print("Valor de depósito inválido. Digite um número positivo.")
                return

            self.saldo += valor_deposito  # Atualiza o saldo (somando o valor do depósito).
            # Registra a transação no extrato
            agora = datetime.datetime.now()
            self.extrato.append({
                "data_hora": agora.strftime("%d/%m/%Y %H:%M:%S"),
                "tipo": "Depósito",
                "valor": valor_deposito
            })
            print(f"Depósito de R$ {valor_deposito:.2f} realizado com sucesso.")
            print(f"Seu novo saldo é: R$ {self.saldo:.2f}")
        except ValueError:
            print("Valor inválido para depósito. Por favor, digite um número.")

    def sacar(self, valor):
        """Realiza uma operação de saque na conta, verificando o saldo."""
        try:
            valor_saque = float(valor)
            if valor_saque <= 0:
                print("Valor de saque inválido. Digite um número positivo.")
                return

            if valor_saque <= self.saldo:  # Verifica se o saldo é suficiente.
                self.saldo -= valor_saque  # Atualiza o saldo
                # Registra a transação no extrato
                agora = datetime.datetime.now()
                self.extrato.append({
                    "data_hora": agora.strftime("%d/%m/%Y %H:%M:%S"),
                    "tipo": "Saque",
                    "valor": valor_saque
                })
                print(f"Saque de R$ {valor_saque:.2f} realizado com sucesso.")
                print(f"Seu novo saldo é: R$ {self.saldo:.2f}")
            else:
                print("Saldo insuficiente.")
        except ValueError:
            print("Valor inválido para saque. Por favor, digite um número.")
    
    def exibir_extrato(self):
        """Exibe o histórico detalhado de transações da conta."""
        if not self.extrato:  # Verifica se o extrato esta vazio
            print("Não foram realizadas transações.")
        else:
            print("\n--- Extrato Bancário ---")
            for transacao in self.extrato:  # Iterar sobre a lista extrato e exiba cada transação formatada.
                data_hora = transacao["data_hora"]
                tipo = transacao["tipo"]
                valor = transacao["valor"]
                print(f"{data_hora} - {tipo}: R$ {valor:.2f}")
            print(f"Saldo atual: R$ {self.saldo:.2f}") # Exibir o saldo atual da conta.
    
    def transferir(self, conta_destino, valor):
        """Realiza uma transferência de valor para outra conta bancária."""
        try:
            valor_transferencia = float(valor)
            if valor_transferencia <= 0:
                print("Valor de transferência inválido. Digite um número positivo.")
                return

            if not isinstance(conta_destino, ContaBancaria): # Verifica se existe a conta de destino
                print("Erro: A conta de destino não é válida de ContaBancaria.")
                return

            if valor_transferencia <= self.saldo: # Verificar se há saldo suficiente na conta de origem
                self.saldo -= valor_transferencia # O valor deve ser subtraído do saldo.
                # Registrar a transação na conta de origem
                agora = datetime.datetime.now()
                self.extrato.append({
                    "data_hora": agora.strftime("%d/%m/%Y %H:%M:%S"),
                    "tipo": f"Transferência para {conta_destino.numero_conta}",
                    "valor": valor_transferencia
                })
                print(f"Transferência de R$ {valor_transferencia:.2f} para conta {conta_destino.numero_conta} realizada com sucesso.")
                print(f"Seu novo saldo é: R$ {self.saldo:.2f}")

                # Chamar o método depositar da conta destino
                conta_destino.depositar(valor_transferencia) # Chamar o método depositar() da conta_destino para adicionar o valor.
            else:
                print("Saldo insuficiente para realizar a transferência.")
        except ValueError:
            print("Valor inválido para transferência. Por favor, digite um número.")

#Exemplo de uso da classe (para testar os métodos adicionados):
if __name__ == "__main__":
    minha_conta = carregar_dados() # Chamar carregar_dados() para obter uma instância de ContaBancaria.

    # Exemplo de como você poderia ter uma segunda conta (para transferência)
    outra_conta = carregar_dados(filename="banco_secundario.json")
    if outra_conta.numero_conta == "00000-0": # Se for uma conta recém-criada (não carregada de arquivo)
        outra_conta.numero_conta = "54321-Y" # Atribui um número real para demonstração

    while True: # Manter o loop while True que exibe o menu de opções.
        print("\n--- Olá! Bem-vindo ao seu banco virtual. ---")
        print("---------------------------------------------")
        print("1 - Consultar Saldo")
        print("2 - Depositar")
        print("3 - Sacar")
        print("4 - Exibir Extrato")
        print("5 - Transferir")
        print("6 - Sair")
        print("---------------------------------------------")
        
        opcao_str = input("Digite a opção desejada: ")
        try:
            opcao = int(opcao_str)
            if not (1 <= opcao <= 6): # Validar a opção escolhida
                print("Opção inválida. Por favor, digite um número entre 1 e 6.")
                continue # Continua o loop para pedir a opção novamente
        except ValueError:
            print("Opção inválida. Por favor, digite um número inteiro.")
            continue

        if opcao == 1:
            minha_conta.consultar_saldo()
        elif opcao == 2:
            valor = input("Digite o valor a depositar: R$ ")
            minha_conta.depositar(valor)
        elif opcao == 3:
            valor = input("Digite o valor a sacar: R$ ")
            minha_conta.sacar(valor)
        elif opcao == 4:
            minha_conta.exibir_extrato()
        elif opcao == 5:
            print(f"Realizando transferência da conta '{minha_conta.numero_conta}' para '{outra_conta.numero_conta}'")
            valor_transferencia = input("Digite o valor a ser transferido: R$ ")
            minha_conta.transferir(outra_conta, valor_transferencia)
        elif opcao == 6:
            salvar_dados(minha_conta) # Salvar os dados da conta principal antes de sair.
            salvar_dados(outra_conta, filename="banco_secundario.json") # Salvar a segunda conta também
            print("Obrigado por utilizar nosso banco virtual!")
        break