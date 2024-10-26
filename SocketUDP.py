from socket import socket, AF_INET, SOCK_DGRAM
import random
import struct

SERVER_ADDR = ("15.228.191.109", 50000)
client_socket = socket(AF_INET, SOCK_DGRAM)

def criar_mensagem(tipo, identificador):
    """Cria uma mensagem de 24 bits com 4 bits para identificar se é de requisição ou resposta, 
    4 bits indicando o tipo de requisição ou resposta e 16 bits para o identificador"""
    mensagem = (0b0000 << 20) | (tipo << 16) | identificador
    return struct.pack('>I', mensagem)[1:]  # Descarte do primeiro byte

def enviar_mensagem(tipo):
    """Gera identificador aleatório, envia mensagem para o servidor e aguarda resposta"""
    identificador = random.randint(1, 65535)
    mensagem = criar_mensagem(tipo, identificador)
    client_socket.sendto(mensagem, SERVER_ADDR)

    resposta, _ = client_socket.recvfrom(1024)
    processar_resposta(resposta, identificador)

def processar_resposta(mensagem, identificador_esperado):
    """Descompacta e valida a resposta, exibindo seu conteúdo se o identificador for correspondente"""
    cabecalho = struct.unpack('>3B', mensagem[:3])  # Extração do cabeçalho
    tipo_resposta = cabecalho[0] & 0b00001111
    identificador_resposta = (cabecalho[1] << 8) | cabecalho[2]
    tamanho_resposta = mensagem[3]

    if identificador_resposta == identificador_esperado:
        conteudo_resposta = mensagem[4:4 + tamanho_resposta]
        if tipo_resposta == 0 or tipo_resposta == 1:
            print(conteudo_resposta.decode())
        elif tipo_resposta == 2:
            print(int.from_bytes(conteudo_resposta, byteorder='big'))
        else:
            print("Resposta inválida")

def cliente():
    """Interface do cliente para solicitar tipos de requisições e enviar para o servidor"""
    opcoes = {
        '1': 0b0000,
        '2': 0b0001,
        '3': 0b0010,
    }

    while True:
        print("\nEscolha uma requisição:\n1. Data e hora atual\n2. Mensagem motivacional\n3. Contagem de respostas\n4. Sair\n")
        escolha = input("Digite o número da requisição: ")

        if escolha in opcoes:
            enviar_mensagem(opcoes[escolha])
        elif escolha == '4':
            print("Saindo...")
            break
        else:
            print("Opção inválida, tente novamente")

if __name__ == "__main__":
    cliente()
    client_socket.close()
