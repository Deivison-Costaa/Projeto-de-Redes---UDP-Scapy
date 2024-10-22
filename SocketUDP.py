from socket import*
import random

serverName =  "15.228.191.109"
serverPort = 50000
clientSocket = socket(AF_INET, SOCK_DGRAM)

while True:
    print("\nEscolha um tipo de requisição (Digite o número correspondente):\n\n")
    print("1. Data e hora atual")
    print("2. Uma mensagem motivacional para o fim do semestre;")
    print("3. A quantidade de respostas emitidas pelo servidor até o momento.")
    print("4. Sair.")
    print("\n\n")

    type = input("Digite o número da requisição.")


    match type:
        case 1:
            reqType = 0;
            iden = random.randint(1, 65535)
              
            
