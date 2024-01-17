from socket import socket, AF_INET, SOCK_STREAM
import argparse
import zipfile
import os
from constants import *
import hashlib

ZIPNAME_LOCAL = "./zipfile.zip"

#Parsea los argumentos de la linea de comandos
def parse_args():
    parser = argparse.ArgumentParser(description='Parser de argumentos')
    
    parser.add_argument('--origin', dest='origin', required=True, help='Directorio origen de los archivos a enviar')
    parser.add_argument('--name', dest='name', required=True, help='Nombre con que se almacena en el servidor')
    parser.add_argument('--ip', dest='ip', required=True, help='Direccion IP del servidor')
    parser.add_argument('--port', dest='port', required=True, help='Puerto del servidor')
    
    config = parser.parse_args()
    config.port = int(config.port)
    
    return config


#Recorre el directorio y sus subdirectorios y genera un archivo zip
def compress(origin, zip_file):
    with zipfile.ZipFile(zip_file, 'w') as zipf:
        for root_dir, _, files in os.walk(origin):
            for f in files:
                fullpath = os.path.join(root_dir, f)
                arcname = os.path.relpath(fullpath, origin)
                zipf.write(fullpath, arcname=arcname)

#Genera el mensaje de inicio
#Es de 100 bytes
    # 57 bytes: nombre con que se almacena en servidor
    # 43 bytes: tamaño del archivo
def init_msg(name):
    #Obtenemos tamaño del archivo
    size = os.path.getsize(ZIPNAME_LOCAL)

    #Generamos mensaje
    msg = name.ljust(INIT_MSG_FILENAME) + str(size).ljust(INIT_MSG_FILESIZE)
    return msg.encode()


# Envia el archivo en bloques de 1024 bytes
def send_file(skt):
    print("[*] Enviando archivo...")

    hash = hashlib.sha1()

    send_bytes = 0
    size = os.path.getsize(ZIPNAME_LOCAL)
    with open(ZIPNAME_LOCAL, 'rb') as f:
        while send_bytes < size:
            data = f.read(BLOCK_SIZE)
            send_bytes += len(data)
            skt.send(data)
            hash.update(data)

    return hash.hexdigest()


def backup(config):
    #Establecemos conexion
    skt = socket(AF_INET, SOCK_STREAM)
    skt.connect((config.ip,config.port))

    #Mensaje de inicio
    msg = init_msg(config.name)
    skt.send(msg)

    #Recibimos ACK
    msg_rcv = skt.recv(1).decode()
    if msg_rcv != "0":
        print("[*] ERROR: El servidor no acepta la subida del archivo.")
        return
    
    #Envio de archivo
    hash = send_file(skt)

    #Recibimos ACK
    msg_rcv = skt.recv(1).decode()
    if msg_rcv != "0":
        print("[*] ERROR: El servidor no acusa recibo.")
        return

    # #Envio de hash
    skt.send(hash.encode())

    # #Recibir respuesta
    msg_rcv = skt.recv(1).decode()
    # print(msg_rcv)
    if msg_rcv != "0":
        print("ERROR: El servidor no pudo guardar el archivo-")
    else:
        print("Archivo enviado correctamente.")

    skt.close()



if __name__ == '__main__':
    config = parse_args()

    #Verificamos que exista el directorio origen
    if not os.path.exists(config.origin):
        print(f"[*] ERROR: No existe el directorio {config.origin}")
        exit(1)

    compress(config.origin, ZIPNAME_LOCAL)

    backup(config)

    os.remove(ZIPNAME_LOCAL)

    
    