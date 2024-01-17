# Backup script

## Funcionamiento
Inicia un servidor que está a la espera de conexiones TCP. El cliente se conecta y envía el directorio al cual desea hacer un backup, que es previamente comprimido y luego enviado en formato .zip.

## Ejecución
### Servidor
```
python3 server.py --port <puerto> --dir <directorio destino>
```
Parámetros:
- port: Puerto donde escuchará conexiones
- dir: Directorio donde se almacenan todos los backups. En caso de no existir, se crea.

### Cliente
```
python3 client.py --origin <directorio origen> --name <nombre> --ip <ip server> --port <puerto server>
```
Parámetros:
- origin: Path al directorio/archivo que queremos respaldar.
- name: Nombre con que se desea guardar en el servidor el directorio/archivo a respaldar.
- ip: Dirección IP donde se conectará el cliente.
- port: Puerto donde se conectará el cliente.


## Protocolo

 cliente &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; servidor  \
________________________ \
  mensaje inicio ---------------->    \
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<--------------------- ACK    \
  mensaje bloque 1 ----------->    \
  mensaje bloque 2 ----------->    \
  mensaje bloque ... ---------->    \
  mensaje bloque n ----------->    \
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<---------------------- ACK    \
  mensaje hash --------------->    \
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<---------------- resultado    

Mensajes:
- Mensaje de inicio (100 bytes): Nombre destino (57 bytes) + Tamaño de archivo en bytes (43 bytes) -> permite hasta 8Tb
- Mensaje ACK (1 byte): 0 (OK, continuar) , 1 (ERROR, abortar)
- Mensaje de bloque (1024 bytes): Bytes del bloque i
- Mensaje de hash SHA1 (40 bytes)
- Mensaje de resultado (1 byte): 0 (OK) , 1 (ERROR)
