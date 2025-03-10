import os
import subprocess
import socket
import time 

def mostrar_menu_principal():
    os.system('clear')
    print("|--------------------------------------------|")
    print("|       MENÚ PRINCIPAL - SERVIDOR TAK        |")
    print("|--------------------------------------------|")
    print("| 1. Instalación del Servidor TAK            |")
    print("|--------------------------------------------|")
    print("| 2. Definir dirección IPv4 privada estática |")
    print("|--------------------------------------------|")
    print("| 3. Definir los puertos del Firewall        |")
    print("|--------------------------------------------|")
    print("| 4. Mostrar certificados existentes         |")
    print("|--------------------------------------------|")
    print("| 5. Crear certificados                      |")
    print("|--------------------------------------------|")
    print("| 6. Eliminar certificados                   |")
    print("|--------------------------------------------|")
    print("| 7. Gestión de usuarios en grupos           |")
    print("|--------------------------------------------|")
    print("| 8. URLs de interés                         |")
    print("|--------------------------------------------|")
    print("| 9. Salir                                   |")
    print("|--------------------------------------------|")

def ejecutar_comando(comando):
    print(f"Ejecutando: {comando}")
    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, check=True)
    print(f"Salida:\n{resultado.stdout}")
    if resultado.stderr:
        print(f"Errores:\n{resultado.stderr}")

def obtener_ip_local():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('8.8.8.8', 80))
        ip_local = s.getsockname()[0]
    except Exception:
        ip_local = '127.0.0.1'
    finally:
        s.close()
    return ip_local

def instalar_tak():
    print("\033[1m\033[32m SE VA A PROCEDER CON LA ISNTALACIÓN AUTOMÁTICA DEL SERVIDOR TAK... \033[0m")
    time.sleep(2)
    ejecutar_comando("sudo apt update && apt full-upgrade -y")
    ejecutar_comando("sudo apt auto-remove -y")
    ejecutar_comando('echo -e "* soft nofile 32768\n* hard nofile 32768" | sudo tee -a /etc/security/limits.conf > /dev/null')
    ejecutar_comando("sudo sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'")
    ejecutar_comando("wget -O- https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/postgresql.org.gpg > /dev/null")
    ejecutar_comando("sudo apt update && apt full-upgrade -y")
    ejecutar_comando("sudo apt auto-remove -y")
    ejecutar_comando("sudo apt install openjdk-17-jre")
    time.sleep(2)
    print("\033[1m\033[32m POR FAVOR, INGRESA EL NOMBRE DEL ARCHIVO INSTALABLE DEL SERVIDOR TAK (.deb): \033[0m")
    ejecutable_tak = input("Nombre del archivo instalable: ").strip()
    if os.path.exists(f"./{ejecutable_tak}"):
        print(f"Instalando el archivo {ejecutable_tak}...")
        ejecutar_comando(f"sudo apt install ./{ejecutable_tak} -y")
    else:
        print(f"\033[1m\033[32m Error: EL ARCHIVO {ejecutable_tak} NO SE ENCUENTRA EN EL DIRECTORIO ACUAL. \033[0m")
        return
    time.sleep(2)
    archivo_metadata = "/opt/tak/certs/cert-metadata.sh"
    print(f"\033[1m\033[32m EDITANDO {archivo_metadata} AUTOMÁTICMENTE... \033[0m")
    time.sleep(1)
    try:
        with open(archivo_metadata, 'a') as file:
            file.write("\n# CONFIGURACIÓN AUTOMÁTICA AÑADIDA POR EL script\n ")
            time.sleep(1)
    except Exception as e:
        print(f"Error al editar {archivo_metadata}: {e}")
    print(f"\033[1m\033[32m ABRIENDO {archivo_metadata} PARA SU EDICIÓN ... \033[0m")
    time.sleep(1)
    os.system(f"sudo nano {archivo_metadata}")
    time.sleep(1)
    ejecutar_comando("sudo systemctl daemon-reload")
    ejecutar_comando("sudo systemctl start takserver.service")
    ejecutar_comando("sudo systemctl enable takserver.service")
    ejecutar_comando("sudo systemctl restart takserver.service")
    time.sleep(1)
    print("\033[1m\033[32m********** ¡ENHORABUENA! INSTALACIÓN DEL SERVIDOR TAK COMPLETADO. **********\033[0m")

def configurar_ipv4_estatica():
    print("033[1m\033[32m A CONTINUACIÓN SE LE VA A FACILITAR UN CONJUNTO DE LINEAS DE COMANDO QUE LE AYUDARÁN CON LA CONFIGURACIÓN DE LA DIRECCIÓN IPv4 PRIVADA ESTÁTICA EN EL DIRECTORIO: /etc/netplan/00-installer-config.yaml. \033[0m")
    time.sleep(3)
    print("EJEMPLO DE CONFIGURACIÓN:\n"
          "network:\n"
          "  version: 2\n"
          "  renderer: NetworkManager\n"
          "  ethernets:\n"
          "    enp0s3:\n"
          "      addresses: [192.168.1.100/24]\n"
          "      gateway4: 192.168.1.1\n"
          "      nameservers:\n"
          "        addresses:\n"
          "          - 8.8.8.8\n"
          "          - 8.8.4.4")
    input("\033[1m\033[32m PRESIONA [INTRO] PARA EDITAR ó [ESCAPE] PARA VOLVER AL MENÚ PRINCIPAL. \033[0m")
    os.system("sudo nano /etc/netplan/00-installer-config.yaml")
    comandos = ["sudo netplan apply", "sudo systemctl restart NetworkManager"]
    for comando in comandos:
        try:
            ejecutar_comando(comando)
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar '{comando}': {e}. VERIFICA LA INSTALACIÓN Y REPITE EL PROCESO NUEVAMENTE.")
            break
        time.sleep(2)
    print("\033[1m\033[32m********** ¡ENHORABUENA! CONFIGURACIÓN DE RED COMPLETADA. **********\033[0m")

def configurar_firewall():
    print("\033[1m\033[32m A CONTINUACIÓN SE VAN A CREAR LAS REGLAS DEL FIREWALL NECESARIAS PARA EL CORRECTO FUNCIONAMIENTO DEL SERVIDOR TAK. \033[0m")
    time.sleep(3)
    print("\033[1m\033[32m CONFIGURANDO EL FIREWALL DEL SERVIDOR TAK ... \033[0m")
    time.sleep(1)
    ejecutar_comando("sudo apt-get install -y ufw")
    ejecutar_comando("sudo ufw enable")
    ejecutar_comando("sudo ufw default deny incoming")
    ejecutar_comando("sudo ufw default allow outgoing")
    ejecutar_comando("sudo ufw allow 8089/tcp")
    ejecutar_comando("sudo ufw allow 8443/tcp")
    ejecutar_comando("sudo ufw status verbose")
    ejecutar_comando("sudo ufw reload")
    time.sleep(1)
    print("\033[1m\033[32m********** ¡ENHORABUENA! CONFIGURACIÓN DEL FIREWALL COMPLETADA. **********\033[0m")

def mostrar_certificados():
    directorio_certificados = "/opt/tak/certs/files"
    
    if not os.path.exists(directorio_certificados):
        print("\033[1m\033[32m********** ¡ NO HAY CERTIFICADOS EXISTENTES ! **********\033[0m")
        input("\033[1m\033[32 PRESIONA [INTRO] PARA VOLVER AL MENÚ PRINCIPAL ... \033[0m")
        return  # Regresar al menú principal
    
    print("\033[1m\033[32 MOSTRANDO TODO EL CONTENIDO DEL DIRECTORIO: /opt/tak/certs/files: \033[0m")
    certificados = os.listdir(directorio_certificados)
    
    if certificados:
        print("Archivos encontrados:")
        for certificado in certificados:
            print(certificado)
    else:
        print("\033[1m\033[32m********** ¡ NO HAY CERTIFICADOS EXISTENTES ! **********\033[0m")
    input("PRESIONA [INTRO] PARA VOLVER AL MENÚ PRINCIPAL ...")

def crear_certificados():
    print("|----------------------------------|")
    print("|    SUBMEÚ - CREAR CERTIFICADOS   |")
    print("|----------------------------------|")
    print("| 1. Crear Autoridad Certificadora |")
    print("|----------------------------------|")
    print("| 2. Crear Certificados Genéricos  |")
    print("|----------------------------------|")
    print("| 3. Atrás                         |")
    print("|----------------------------------|")
    opcion = input("SELECCIONE UNA OPCIÓN: ")
    if opcion == "1":
        print("\033[1m\033[32m A CONTINUACIÓN SE VA A CREAR EL CERTIFICADO DE AUTORIDAD CERTIFICADORA, ESTE PROCESO JAMÁS DEBES REPETIRLO, DE LO CONTRARIO SE PRODUCIRÁ UN CONFLICTO DE AUTORIDADES EN EL SERVIDOR TAK \033[0m")
        print("\033[1m\033[32m ¿CÓMO DESEA NOMBRAR AL CERTIFICADO DE AUTORIDAD CERTIFICADORA? Consejo: rootca \033[0m")
        ejecutar_comando("cd /opt/tak/certs && ./makeRootCa.sh")
        ejecutar_comando("sudo systemctl restart takserver.service")
        time.sleep(1)
        print("\033[1m\033[32m********** ¡ CERTIFICADO DE [AUTORIDAD CERTIFICADORA] CREADO CORRECTAMENTE ! **********\033[0m")
    elif opcion == "2":
        print("\033[1m\033[32m A CONTNINUACIÓN PODRÁ CREAR CERTIFICADOS DE CLIENTE O SERVIDOR. EN CASO DE QUE QUIERA CREAR UN CERTIFICADO DE SERVIDOR JAMÁS REPITA EL PROCESO, DE LO CONTRARIO SE PRODUCIRÁ UN CONFLICTO DE CERTIFICADOS EN EL SERVIDOR TAK. \033[0m")
        tipo_certificado = input("\033[1m\033[32m DEFINA EL TIPO DE CERTIFICADO QUE DESEA CREAR(client/server): \033[0m")
        nombres_certificados = input("\033[1m\033[32m ¿CÓMO DESEA NOMBRAR AL CERTIFICADO ESCOGIDO?, EN CASO DE QUERER CREAR VARIOS CERTIFICADOS DE USUARIO, SEPARALOS POR COMAS (,): \033[0m")
        for nombre in nombres_certificados.split(","):
            ejecutar_comando(f"cd /opt/tak/certs && ./makeCert.sh {tipo_certificado} {nombre}")
            ejecutar_comando("sudo systemctl restart takserver.service")
            time.sleep(1)
        print("\033[1m\033[32m********** ¡ CERTIFICADO(s) CREADO(s) CORRECTAMENTE ! **********\033[0m")
    elif opcion == "3":
        return
    else:
        print("\033[1m\033[32m********** ¡ OPCIÓN INVÁLIDA ! **********\033[0m")

def eliminar_certificados():
    certificado = input("\033[1m\033[32m INDIQUE EL NOMBRE DEL [CERTIFICADO] QUE DESEA ELIMINAR (sin extensión): \033[0m").strip()
    extensiones = ['.csr', '.jks', '.key', '.p12', '.pem', '-trusted.pem']
    
    archivos_existentes = []
    for ext in extensiones:
        archivo = f"/opt/tak/certs/files/{certificado}{ext}"
        if os.path.isfile(archivo):
            archivos_existentes.append(archivo)
    
    if archivos_existentes:
        print("CERTIFICADO ENCONTRADO, ELIMINANDO ...")
        for archivo in archivos_existentes:
            print(f"ELIMINANDO: {archivo}")
            os.remove(archivo)
            ejecutar_comando("sudo systemctl restart takserver.service")
            time.sleep(1)
        print("\033[1m\033[32m********** ¡ CERTIFICADO ELIMINADO CORRECTAMENTE ! **********\033[0m")    
    else:
        print(f"NO SE HA ENCONTRADO EL CERTIFICADO '{certificado}' EN LAS EXTENSIONES PREDETERMMINADAS.")

def gestionar_usuarios():
    print("|--------------------------------------------|")
    print("|  SUBMEÚ - GESTIÓN DE USUARIOS EN GRUPOS    |")
    print("|--------------------------------------------|")
    print("| 1. Agregar un certificado a un grupo       |")
    print("|--------------------------------------------|")
    print("| 2. Desagregar un certificado de un grupo   |")
    print("|--------------------------------------------|")
    print("| 3. Atrás                                   |")
    print("|--------------------------------------------|")
    opcion = input("SELECCIONE UNA OPCIÓN: ")
    if opcion == "1":
        certificado = input("INGRESE EL NOMBRE DEL CERTIFICADO: ")
        if os.path.isfile(f"/opt/tak/certs/files/{certificado}.pem"):
            print("\033[1m\033[32m********** ¡ CERTIFICADO ENCONTRADO ! **********\033[0m")
            print("|----------------------------|")
            print("| 1. Grupo de Administración |")
            print("|----------------------------|")
            print("| 2. Otros grupos            |")
            print("|----------------------------|")
            subopcion = input("SELECCIONE UNA OPCIÓN: ")
            if subopcion == "1":
                ejecutar_comando(f"java -jar /opt/tak/utils/UserManager.jar certmod -A /opt/tak/certs/files/{certificado}.pem")
                print("\033[1m\033[32m********** ¡ [CERTIFICADO] AGREGADO AL [GRUPO] DE ADMINISTRACIÓN ! **********\033[0m")
            elif subopcion == "2":
                tipo_grupo = input("\033[1m\033[32m INDIQUE EL TIPO DE [GRUPO]: (Entrada/Salida/Ambas): \033[0m")
                if tipo_grupo == "Entrada":
                    grupo = input("\033[1m\033[32m INDIQUE EL NOMBRE DEL [GRUPO]: \033[0m")
                    ejecutar_comando(f"java -jar /opt/tak/utils/UserManager.jar certmod -ig{grupo} /opt/tak/certs/files/{certificado}.pem")
                elif tipo_grupo == "Salida":
                    grupo = input("\033[1m\033[32m INDIQUE EL NOMBRE DEL [GRUPO]: \033[0m")
                    ejecutar_comando(f"java -jar /opt/tak/utils/UserManager.jar certmod -og{grupo} /opt/tak/certs/files/{certificado}.pem")
                elif tipo_grupo == "Ambas":
                    grupo = input("\033[1m\033[32m INDIQUE EL NOMBRE DEL [GRUPO]: \033[0m")
                    ejecutar_comando(f"java -jar /opt/tak/utils/UserManager.jar certmod -g{grupo} /opt/tak/certs/files/{certificado}.pem")
            else:
                print("\033[1m\033[32m********** ¡ OPCIÓN INVÁLIDA ! **********\033[0m")
        else:
            print("\033[1m\033[32m********** ¡ [CERTIFICADO] NO ENCONTRADO ! **********\033[0m")
    elif opcion == "2":
        certificado = input("\033[1m\033[32m INGRESE EL NOMBRE DEL [CERTIFICADO]: \033[0m")
        if os.path.isfile(f"/opt/tak/certs/files/{certificado}.pem"):
            ejecutar_comando(f"java -jar /opt/tak/utils/UserManager.jar certmod -r /opt/tak/certs/files/{certificado}.pem")
            print("\033[1m\033[32m********** ¡ [CERTIFICADO] ELIMINADO DEL [GRUPO] ! **********\033[0m")
        else:
            print("\033[1m\033[32m********** ¡ [CERTIFICADO] NO ENCONRTADO ! **********\033[0m")
    elif opcion == "3":
        return
    else:
        print("\033[1m\033[32m********** ¡ OPCIÓN INVÁLIDA ! **********\033[0m")

def mostrar_urls():
    print("URLs DE INTERÉS:")
    print("TAK HERRAMIENTA DE ADMINISTRACIÓN WEB: https://localhost:8443/Matri/metrics/index.html")
    print("SERVIDOR TAK: https://localhost:8443/webtak/index.html")

def main():
    while True:
        mostrar_menu_principal()
        opcion = input("SELECCIONE UNA OPCIÓN: ")
        if opcion == "1":
            instalar_tak()
        elif opcion == "2":
            configurar_ipv4_estatica()
        elif opcion == "3":
            configurar_firewall()
        elif opcion == "4":
            mostrar_certificados()
        elif opcion == "5":
            crear_certificados()
        elif opcion == "6":
            eliminar_certificados()
        elif opcion == "7":
            gestionar_usuarios()
        elif opcion == "8":
            mostrar_urls()
        elif opcion == "9":
            print("\033[1m\033[32m********** ¡ GRACIAS POR USAR NUESTRA APLICACIÓN ! **********\033[0m")
            print("\033[1m\033[32m********** ¡ VUELVE CUANDO QUIERAS ! **********\033[0m")
            break
        else:
            print("\033[1m\033[32m********** ¡ OPCIÓN INVÁLIDA ! **********\033[0m")
        input("PRESIONA [INTRO] PARA CONTINUAR...")

if __name__ == "__main__":
    main()
