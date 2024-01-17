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
