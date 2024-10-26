from scapy.all import*

def cliente():
    
    pacote = IP(dst="15.228.191.109") / UDP(sport= 62123, dport=50000) / Raw(load=0x000003)
    algo = sr1(pacote)
    
    print(algo)


if __name__ == "__main__":
    cliente()

