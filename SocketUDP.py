from socket import*
import random
import struct

addr = ("15.228.191.109", 50000)

client_socket = socket(AF_INET, SOCK_DGRAM) 

def criar_mensagem(tipo, identificador_resposta):
    mensagem = (0b0000 << 20) | (tipo << 16) | identificador_resposta # Criando a mensagem de 24 bits
    # 4 bits para o req/res, 4 bits para o tipo e 16 bits para o identificador
    return struct.pack('>I', mensagem)[1:] # Removendo o primeiro byte

def enviar_mensagem(tipo):
    identificador_mensagem = random.randint(1, 65535)
    mensagem = criar_mensagem(tipo, identificador_mensagem)
    client_socket.sendto(mensagem, addr)

    resposta, _ = client_socket.recvfrom(1024)
    
    resposta_mensagem(resposta, identificador_mensagem)


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
    client_socket.close()