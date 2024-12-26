       git clone https://github.com/casper0169/TAKSERVER
       chmod 777 * 
       cd TAKSERVER/
       chmod 777 *

El Menú que se abrirá permitirá elegir entre estas opciones:

1.- Se ejecutará automáticamente la instalación del Servidor TAK, pero necesitas tener el documento takserver_5.3-RELEASE4_all.deb (o similar) en la carpeta (TAKSERVER/)

2.- Se configura la tarjeta de red enp0s3 con los valores que se mostrarán en la plantilla o con los que tu quieras editar

3.- Se configuran los parámetros del firewall (8089 y 8443 /tcp) por defecto de manera automática

4.- Muestra los certificados existentes en el directorio /opt/tak/certs/files

5.- Crea certificados de varios tipos:
- Autoridad Certificadora (CA)
- Cliente ó Servidor

6.- Elmina todos los certificados del directorio op/tak/certs/files junto con sus extensiones de archivo

7.- Gestiona los certificados en cada grupo:
- Administrador
- Otros grupos
       - Entrada, Salida ó Ambos
- Elimina certificados de grupos

8.- Muestra las URLs de interés:
- https://localhost:8443/webtak/index.html
- https://localhost:8443/Matri/metrics/index.html

9.- Cierra el programa
