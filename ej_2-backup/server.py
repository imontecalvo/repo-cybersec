from socket import socket, AF_INET, SOCK_STREAM
import argparse
from constants import *
import hashlib
import os

reset = "\033[0m"
red = "\033[91m"
green = "\033[92m"
cyan = "\033[96m"

#Parsea los argumentos de la linea de comandos
def parse_args():
    parser = argparse.ArgumentParser(description='Parser de argumentos')
    
    parser.add_argument('--dir', dest='dir', required=True, help='Directorio donde se almacenan los backups')
    parser.add_argument('--port', dest='port', required=True, help='Puerto del servidor')
    
    config = parser.parse_args()
    config.port = int(config.port)
    
    return config

#Parsea el mensaje de inicio
def parse_init_msg(msg):
    name = msg[:INIT_MSG_FILENAME].strip()
    size = int(msg[INIT_MSG_FILENAME:INIT_MSG_FILENAME+INIT_MSG_FILESIZE])
    return name, size

#Imprime feedback de la recepcion del archivo
def feedback(rcv_bytes, lendata, size):
    FOLDS = 5
    fold = size / FOLDS
    for i in range(1,FOLDS):
        if rcv_bytes >= fold*i and rcv_bytes-lendata < fold*i:
            print(f"[*] Se han recibido {rcv_bytes}/{size} - {cyan}{round(rcv_bytes/size*100,2)} %{reset}")
            break

#Recibe el archivo en bloques de 1024 bytes
def receive_file(conn, config, name, size):
    hash = hashlib.sha1()
    with open(f"{config.dir}/{name}", 'wb') as f:
        rcv_bytes = 0
        while rcv_bytes < size:
            data = conn.recv(BLOCK_SIZE)
            rcv_bytes += len(data)
            f.write(data)
            hash.update(data)
            feedback(rcv_bytes, len(data),size)
    
    return hash.hexdigest()


def listen(config):
    #Establecemos conexion
    skt = socket(AF_INET, SOCK_STREAM)
    skt.bind(('', config.port))
    skt.listen(0)

    print("[*] Servidor escuchando conexiones...")

    while True:
        #Esperando que se conecte un cliente
        conn, addr = skt.accept()
        print(f"\n[*] Nueva conexión desde {addr[0]}:{addr[1]}")

        #Recepcion de mensaje de inicio
        msg_rcv = conn.recv(INIT_MSG_SIZE).decode()
        name, size = parse_init_msg(msg_rcv)
        
        #Enviamos ACK
        conn.send("0".encode())

        #Recepcion de archivo
        hash = receive_file(conn, config, name, size)
        
        #Envio de ACK
        conn.send("0".encode())

        #Recepcion de hash
        hash_rcv = conn.recv(HASH_SIZE).decode()

        #Envio de Resultado
        if hash == hash_rcv:
            print(f"[*] Se ha recibido el archivo {name} correctamente - {cyan}100%{reset}")
            print(f"{green}SHA1: {hash}{reset} ✔")
            conn.send("0".encode())
        else:
            print(f"[*] Error en la recepción del archivo {name}")
            print(f"{red}SHA1 esperado: {hash_rcv}\nSHA1 obtenido: {hash}{reset} ✘")
            conn.send("1".encode())

        #Cerramos conexion
        conn.close()


if __name__ == '__main__':
    config = parse_args()

    #Verificamos puerto
    if config.port < 1024 or config.port > 65535:
        print(f"[*] ERROR: El puerto {config.port} no se encuentra en el rango permitido (1024-65535)")
        exit(1)

    #Verificamos que exista el directorio destino
    if not os.path.exists(config.dir):
        os.makedirs(config.dir)

    listen(config)
