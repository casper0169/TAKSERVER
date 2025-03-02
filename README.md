## Copiar el repositorio y acceder a su contenido
       
       git clone https://github.com/casper0169/TAKSERVER
       chmod 777 * 
       cd TAKSERVER/
       chmod 777 *
       python3 ATAK.py

## Breve resumen del contenido
       
El uso del programa ATAK.py resulta extremadamente eficaz para automatizar la Instalación, al mismo tiempo se pueden seguir los pasos indicados en el documento Instalación del Takserver oficial.pdf, ya que el documento Preparacion de la Maquina Virtual - 1.pdf está destinado a la creación de la Máquina Virtual que albergará el Servidor TAK y su personalización más básica (TAK wallpaper.png como imagen de usuario y bandera españa + TAK.png para usarla de fondo de pantalla del servidor)

El Menú que se abrirá permitirá elegir entre estas opciones:

1.- Se ejecutará automáticamente la instalación del Servidor TAK, pero necesitas tener el documento takserver_5.3-RELEASE4_all.deb (que lo encontrarás en el apartado: Enlace de Google Drive para descargar los recursos 👇)

2.- Se configura la tarjeta de red enp0s3 con los valores que se mostrarán en la plantilla o con personalización libre

3.- Se configuran los parámetros del firewall (8089 y 8443 /tcp) por defecto de manera automática

4.- Muestra los certificados existentes en el directorio /opt/tak/certs/files (si los hay)

5.- Crea certificados de varios tipos:
- Autoridad Certificadora (CA)
- Cliente ó Servidor

6.- Elmina todos los certificados del directorio op/tak/certs/files junto con sus extensiones de archivo (pero no los revoca)

7.- Gestiona los certificados en cada grupo:
- Administrador web
- Otros grupos
       - Entrada, Salida ó Ambos
- Elimina certificados de grupos

8.- Muestra las URLs de interés:
- https://localhost:8443/Matri/metrics/index.html
- https://localhost:8443/webtak/index.html

9.- Cierra el programa

## Enlace de Google Drive para descargar los recursos 👇
https://drive.google.com/drive/folders/1hiVebNQwVulF26Do28aj8Jov90cyAzny?usp=drive_link

## ⚔🦅Video Automatización TAK SERVER ⚔🦅
[![Ver Video](https://img.youtube.com/vi/im2YOjh49EE/0.jpg)](https://youtu.be/im2YOjh49EE)




