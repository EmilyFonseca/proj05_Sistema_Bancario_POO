# proj05_Sistema_Bancario_POO
#  Simulador de Sistema Bancario com Programação Orientada a Objetos (POO)

Este projeto consiste em um sistema bancário em Python que simula as principais operações de um caixa eletrônico. Diferente da versão anterior, esta implementação aplica os princípios da **Programação Orientada a Objetos (POO)**, promovendo modularidade, clareza e facilidade de manutenção e expansão do código.

---

##  Objetivos

Desenvolvimento de um programa que simule as operações básicas de um caixa eletrônico, utilizando os princípios de Orientação a Objetos.

---

##  Funcionalidades

O sistema simula as seguintes operações bancárias:

###  Consulta de Saldo
- Exibe o saldo atual da conta.

###  Saque
- Permite ao usuário sacar um valor.
- Verifica se há saldo suficiente antes de concluir a operação.

###  Depósito
- Permite ao usuário depositar qualquer valor positivo.

###  Extrato Detalhado
- Mostra uma lista com todas as transações realizadas: saques, depósitos e transferências.

###  Transferência entre Contas
- Permite transferir valores de uma conta para outra existente no sistema.

###  Persistência de Dados com JSON
- O saldo e o extrato são salvos em um arquivo `.json`, garantindo que as informações sejam mantidas mesmo após o programa ser encerrado.

###  Menu Interativo
- Interface no terminal com opções numéricas.
- Validação robusta para impedir entradas inválidas.

