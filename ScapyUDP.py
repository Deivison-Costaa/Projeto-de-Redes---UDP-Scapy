#from socket import*
import random
import struct
from scapy.all import *
#import socket

#client_socket = socket(AF_INET, SOCK_DGRAM)

# def ip_local():
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.connect("10.255.255.255", 1)
#         ip = s.getsockname()[0]
#         s.close()
#         return ip
#     except Exception as e:
#         return f"Erro ao obter IP: {e}"


def ip_para_ints(ip_str):
    octetos = list(map(int, ip_str.split('.')))
    if len(octetos) != 4 or any(octeto < 0 or octeto > 255 for octeto in octetos):
        raise ValueError("IP inválido. Certifique-se de que ele esteja no formato correto.")
    
    ip_32bits = (octetos[0] << 24) | (octetos[1] << 16) | (octetos[2] << 8) | octetos[3]     # Converter o IP para uma sequência de 32 bits

    # Extrair os 16 bits mais significativos e os 16 bits menos significativos
    parte_mais_significativa = (ip_32bits >> 16) & 0xFFFF
    parte_menos_significativa = ip_32bits & 0xFFFF

    return parte_mais_significativa, parte_menos_significativa




def calcular_checksum(UDP, IP, pacote):
    soma = sum(UDP.values()) + IP['proto'] + IP['len'] #soma os valores fixos
    print(bin(soma) + " " + hex(soma))
    
    ip_src_s, ip_src_ms = ip_para_ints(IP['src'])
    ip_dst_s, ip_dst_ms = ip_para_ints(IP['dst'])
    
    print(ip_src_s + ip_src_ms + ip_dst_s + ip_dst_ms)
    
    soma += ip_src_s + ip_src_ms + ip_dst_s + ip_dst_ms # soma os ips
    
    print(soma)
    print(hex(pacote) + " " + bin(pacote))
    
    pacote = pacote << 8  # Desloca 8 bits para a esquerda
    bma_s = (pacote >> 16) & 0xFFFF
    bme_s = pacote & 0xFFFF
    
    print(f"{bin(bma_s)}  :  {bin(bme_s)}")
    
    soma += bma_s + bme_s #soma os pacotes
    
    print(bin(soma))
    
    while soma >> 16:  # Enquanto houver overflow (desloca 16 bits a direita)
        soma = (soma & 0xFFFF) + (soma >> 16) #soma os 16 bits menos significativos com os bits alem de 16 bits
    
    print(bin(soma))
    
    soma = ~soma & 0xFFFF
    print(bin(soma))
    
    return soma
    
    

def criar_mensagem(tipo, identificador_resposta):
    mensagem =  (tipo << 16) | identificador_resposta # Criando a mensagem de 24 bits
    
    # 4 bits para o req/res, 4 bits para o tipo e 16 bits para o identificador
    print(hex(mensagem))
    return mensagem

def enviar_mensagem(tipo):
    identificador_mensagem = random.randint(1, 65535)
    mensagem = criar_mensagem(tipo, identificador_mensagem)
    print(bin(mensagem))
    
    UDP_kanxa = {
        'dport':  50001, #random.randint(45000, 55000),
        'sport': 50000,
        'len': 11,
        'chksum': 0
    }
    
    IP_kanxa = {
        'src': "192.168.1.105",
        'dst': "15.228.191.109",
        'proto': 17,
        'len': 11
    }
    
    UDP_kanxa['chksum'] = calcular_checksum(UDP_kanxa, IP_kanxa, mensagem)
    print(UDP_kanxa['chksum'])
    
    pacote = IP(dst= IP_kanxa['dst']) / UDP(sport= UDP_kanxa['sport'], dport=UDP_kanxa['dport'], len=UDP_kanxa['len'], chksum=UDP_kanxa['chksum']) / Raw(load=mensagem)
    
    resposta = sr1(pacote)
    
    resposta_mensagem(resposta, identificador_mensagem)
    
    

def resposta_mensagem(mensagem, identificador_mensagem):
    cabecalho = struct.unpack('>3B', mensagem[:3]) # 3 bytes do cabeçalho
    tipo_resposta = (cabecalho[0] & 0b00001111) # and bit a bit para pegar apenas os 4 bits referentes ao tipo
    identificador_resposta = (cabecalho[1] << 8) | cabecalho[2]  # Identificador de 2 bytes
    tamanho_resposta = mensagem[3]
    
    if identificador_mensagem == identificador_resposta: #ve se o identificador bate
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
            enviar_mensagem(0x00)
        elif num == '2':
            enviar_mensagem(0x01)
        elif num == '3':
            enviar_mensagem(0x02)
        elif num == '4':
            print("Saindo...")
            break
        else:
            print("Opção inválida")
            
            
if __name__ == "__main__":
    # print(ip_local)
    cliente()
    #client_socket.close()
