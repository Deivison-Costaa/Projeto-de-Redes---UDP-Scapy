#from socket import*
import random
import struct
from scapy.all import *

ipServer = "15.228.191.109"
dport = 50000
sport = 50001
mac_dest = "e0:e8:e6:d8:64:0d"

#client_socket = socket(AF_INET, SOCK_DGRAM)

def calcular_checksum(data):
    """
    Calcula o checksum de 16 bits para a sequência de bytes fornecida com wraparound.

    Args:
        data (bytes): Dados para os quais o checksum deve ser calculado.

    Returns:
        int: Valor do checksum em formato numérico.
    """
    soma = 0  # Inicializa a soma
    n = len(data)  # Comprimento dos dados

    # Soma bytes em pares
    for i in range(0, n, 2):
        # Pega dois bytes, o segundo byte é deslocado 8 bits para a esquerda
        if i + 1 < n:
            par = data[i] + (data[i + 1] << 8)  # Combina dois bytes
        else:
            par = data[i]  # Caso haja um byte solitário
        
        soma += par  # Adiciona à soma

        # Aplica o wraparound
        while soma > 0xFFFF:
            soma = (soma & 0xFFFF) + 1  # Adiciona 1 ao excesso

    # Retorna o complemento
    return ~soma & 0xFFFF  # Complemento de 1

def criar_mensagem(tipo, identificador_resposta):
    mensagem = (0b0000 << 20) | (tipo << 16) | identificador_resposta # Criando a mensagem de 24 bits
    # 4 bits para o req/res, 4 bits para o tipo e 16 bits para o identificador
    return struct.pack('>I', mensagem)[1:] # Removendo o primeiro byte

def enviar_mensagem(tipo):
    identificador_mensagem = random.randint(1, 65535)
    mensagem = criar_mensagem(tipo, identificador_mensagem)
    
    #client_socket.sendto(mensagem, addr)
    # pacote_udp = UDP(sport=sport, dport=dport)
    # pacote_ip = IP(dst=ipServer)
    #resposta, _ = client_socket.recvfrom(1024)
    pacote_completo = IP(src="150.165.134.68", dst=ipServer, proto = 17) / UDP(sport=sport, dport=dport, len = len(mensagem) + 8) / mensagem
    pacote_completo.show()
    send(pacote_completo)
    sr1(pacote_completo, timeout=5)
    
    #resposta_mensagem(resposta, identificador_mensagem)


def resposta_mensagem(mensagem, identificador_mensagem):
    cabecalho = struct.unpack('>3B', mensagem[:3]) # 3 bytes do cabeçalho
    tipo_resposta = (cabecalho[0] & 0b00001111) # and bit a bit para pegar apenas os 4 bits referentes ao tipo
    identificador_resposta = (cabecalho[1] << 8) | cabecalho[2]  # Identificador de 2 bytes
    tamanho_resposta = mensagem[3]
    
    if identificador_mensagem == identificador_resposta: # verificação para garantia de resposta a mensagem correta
        match tipo_resposta:
            case 0:
                conteudo_resposta = mensagem[4:4 + tamanho_resposta].decode()
                print(conteudo_resposta)
            case 1:
                conteudo_resposta = mensagem[4:4 + tamanho_resposta].decode()
                print(conteudo_resposta)
            case 2:
                conteudo_resposta = mensagem[4:4 + tamanho_resposta]
                print(int.from_bytes(conteudo_resposta, byteorder='big'))
            case _:
                print("Resposta inválida")
    

def cliente():

    while True:
        print("\nEscolha um tipo de requisição (Digite o número correspondente):\n\n")
        print("1. Data e hora atual")
        print("2. Uma mensagem motivacional para o fim do semestre;")
        print("3. A quantidade de respostas emitidas pelo servidor até o momento.")
        print("4. Sair.")
        print("\n\n")

        num = input("Digite o número da requisição: ")
        print(f"valor recebido {num}")
        
        if num == '1':
            enviar_mensagem(0b0000)
        elif num == '2':
            enviar_mensagem(0b0001)
        elif num == '3':
            enviar_mensagem(0b0010)
        elif num == '4':
            print("Saindo...")
            break
        else:
            print("Opção inválida")
            
            
if __name__ == "__main__":
    cliente()
    #client_socket.close()
