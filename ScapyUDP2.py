from scapy.all import *
import random
import struct

# Definições de IP e porta do servidor
# SERVER_IP = "15.228.191.109"
# SERVER_PORT = 50000
# CLIENT_PORT = random.randint(50000, 60000)


# def calcular_checksum(udp_header, ip_header, pacote):
    
#     udp_sum = udp_header.src[:2] + udp_header.src[2:] + udp_header.dst[:2] + udp_header.dst[2:] + udp_header.proto + udp_header.len
#     ip_sum = ip_header.sport + ip_header.dport + ip_header.len + ip_header.chksum
#     pacote = pacote + bytes([0b00000000])
#     pack1 = pacote[:2]
#     pack2 = pacote[2:]
    
#     sum_total = udp_sum + ip_sum + pack1 + pack2
    
#     # Calcula o checksum
#     return checksum(full_packet)
    

def calcular_checksum(udp_header, ip_header, pacote):
    # Constrói o pseudo-cabeçalho para o UDP
    pseudo_header = struct.pack('!4s4sHHH', 
                                ip_header.src,      # Endereço IP de origem (4 bytes)
                                ip_header.dst,      # Endereço IP de destino (4 bytes)
                                ip_header.chksum,   # Zero
                                0x0011,   # Protocolo (2 byte)
                                udp_header.len)     # Comprimento do UDP (2 bytes)
    
    # Constrói o cabeçalho UDP
    udp_header_bytes = struct.pack('!HHHH', 
                                    udp_header.sport,    # Porta de origem
                                    udp_header.dport,    # Porta de destino
                                    udp_header.len,      # Comprimento do UDP
                                    0)                   # Checksum inicial (0)
    
    # Adiciona o pacote e o byte adicional (0)
    pacote_modificado = pacote + bytes([0b00000000])
    # Cria um buffer que inclui o pseudo cabeçalho, cabeçalho UDP e o pacote
    dados = pseudo_header + udp_header_bytes + pacote_modificado

    # Realiza a soma em conjuntos de 16 bits
    soma = 0
    for i in range(0, len(dados), 2):
        # Pega os 2 bytes
        if i + 1 < len(dados):
            dois_bytes = (dados[i] << 8) + dados[i + 1]
        else:
            dois_bytes = (dados[i] << 8)  # Para o último byte, adiciona um zero
        soma += dois_bytes
        soma = (soma & 0xFFFF) + (soma >> 16)  # Adiciona o carry

    # Inverte a soma (complemento de um)
    checksum_result = ~soma & 0xFFFF
    
    return checksum_result



def criar_mensagem(tipo, iden):
    if tipo == 0:
        pack = bytes([0b00000000]) + iden.to_bytes(2, byteorder='big')
    elif tipo == 1:
        pack = bytes([0b00000001]) + iden.to_bytes(2, byteorder='big')
    elif tipo == 2:
        pack = bytes([0b00000010]) + iden.to_bytes(2, byteorder='big')
    else:
        print("Tipo Invalido")
        return None  # Retorna None se o tipo for inválido
        
    return pack

        
        

def requisicao(tipo):
    iden = random.randint(1, 65535)
    pacote = criar_mensagem(tipo, iden)
    
    udp_kanxa = UDP(
        sport=0xE713,
        dport=0xC350,
        len= 0x000B,
        chksum= 0x0000  # Inicialmente o checksum é 0
    )
    
    ip_kanxa = IP(
        src = 0xC0A86502,  # mutavel
        dst = 0x0FE4BF6D, # imutavel
        # proto = 0x0011, # imutavel
        len= 0x000B # imutavel
    )
    
    udp_kanxa.chksum = calcular_checksum(udp_kanxa, ip_kanxa, pacote)
    
    pacote_total = udp_kanxa / ip_kanxa / pacote
    pacote_total.show()
    resposta = sr1(pacote_total, timeout=5)
    print(f"{resposta}")
    


if __name__ == "__main__":
    print("Escolha o tipo de requisição:")
    print("1 - Data e hora atual")
    print("2 - Mensagem motivacional para o fim do semestre")
    print("3 - Quantidade de respostas emitidas pelo servidor")
    print("4 - Sair")

    while True:
        opcao = int(input("Digite uma opção: "))
        if opcao == 1:
            requisicao(0)
        elif opcao == 2:
            requisicao(1)
        elif opcao == 3:
            requisicao(2)
        elif opcao == 4:
            print("Saindo...")
            break
        else:
            print("Opção inválida.")
