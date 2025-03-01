import os
import subprocess
import socket
import time  # Importado para manejar el intervalo entre comandos

def mostrar_menu_principal():
    os.system('clear')
    print("|============================================|")
    print("|       MENÚ PRINCIPAL - SERVIDOR TAK        |")
    print("|============================================|")
    print("| 1. Instalación del Servidor TAK            |")
    print("| 2. Definir dirección IPv4 privada estática |")
    print("| 3. Definir los puertos del Firewall        |")
    print("| 4. Mostrar certificados existentes         |")
    print("| 5. Crear certificados                      |")
    print("| 6. Eliminar certificados                   |")
    print("| 7. Gestión de usuarios en grupos           |")
    print("| 8. URLs de interés                         |")
    print("| 9. Salir                                   |")
    print("|============================================|")

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
    print("Instalando Servidor TAK automáticamente...")
    ejecutar_comando("sudo apt update && apt full-upgrade -y")
    ejecutar_comando("echo '* soft nofile 32768\n* hard nofile 32768' | sudo tee -a /etc/security/limits.conf > /dev/null")
    ejecutar_comando("sudo mkdir -p /etc/apt/keyrings")
    ejecutar_comando("sudo curl https://www.postgresql.org/media/keys/ACCC4CF8.asc --output /etc/apt/keyrings/postgresql.asc")
    ejecutar_comando("sudo sh -c 'echo \"deb [signed-by=/etc/apt/keyrings/postgresql.asc] http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main\" > /etc/apt/sources.list.d/postgresql.list'")
    ejecutar_comando("sudo apt install -y openjdk-17-jdk")
    ejecutar_comando("sudo add-apt-repository ppa:openjdk-r/ppa -y")
    ejecutar_comando("sudo apt update && sudo apt full-upgrade -y")
    ejecutar_comando("sudo update-alternatives --config java")
    ejecutar_comando("sudo apt install -y maven gradle")
    time.sleep(2)
    print("Por favor, ingresa el nombre del archivo instalable del servidor TAK (por ejemplo, 'takserver-installer.deb'): ")
    ejecutable_tak = input("Nombre del archivo instalable: ").strip()
    if os.path.exists(f"./{ejecutable_tak}"):
        print(f"Instalando el archivo {ejecutable_tak}...")
        ejecutar_comando(f"sudo apt install ./{ejecutable_tak}")
    else:
        print(f"Error: El archivo {ejecutable_tak} no se encuentra en el directorio.")
        return
    ejecutar_comando("sudo systemctl daemon-reload")
    ejecutar_comando("sudo systemctl start takserver")
    ejecutar_comando("sudo systemctl enable takserver")
    ejecutar_comando("sudo systemctl restart takserver")
    time.sleep(2)
    archivo_metadata = "/opt/tak/certs/cert-metadata.sh"
    print(f"Editando {archivo_metadata} automáticamente...")
    try:
        with open(archivo_metadata, 'a') as file:
            file.write("\n# Configuración automática añadida por el script\n")
    except Exception as e:
        print(f"Error al editar {archivo_metadata}: {e}")
    print(f"Abriendo {archivo_metadata} para su edición...")
    os.system(f"sudo nano {archivo_metadata}")
    print("\033[1m\033[32m********** ¡ENHORABUENA! INSTALACIÓN DEL SERVIDOR TAK COMPLETADO. **********\033[0m")

def configurar_ipv4_estatica():
    print("Configura la dirección IPv4 privada estática en /etc/netplan/00-installer-config.yaml.")
    print("Ejemplo de configuración:\n"
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
    input("Presiona INTRO para editar o ESCAPE para volver al menú principal.")
    os.system("sudo nano /etc/netplan/00-installer-config.yaml")
    comandos = ["sudo netplan apply", "sudo systemctl restart NetworkManager"]
    for comando in comandos:
        try:
            ejecutar_comando(comando)
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar '{comando}': {e}. Verifica la configuración e intenta nuevamente.")
            break
        time.sleep(2)
    print("\033[1m\033[32m********** ¡ENHORABUENA! CONFIGURACIÓN DE RED COMPLETADA. **********\033[0m")

def configurar_firewall():
    print("Configurando el Firewall...")
    ejecutar_comando("sudo apt-get install -y ufw")
    ejecutar_comando("sudo ufw enable")
    ejecutar_comando("sudo ufw allow 8089/tcp")
    ejecutar_comando("sudo ufw allow 8443/tcp")
    ejecutar_comando("sudo ufw status verbose")
    ejecutar_comando("sudo ufw reload")
    print("\033[1m\033[32m********** ¡ENHORABUENA! CONFIGURACIÓN DEL FIREWALL COMPLETADA. **********\033[0m")

def mostrar_certificados():
    directorio_certificados = "/opt/tak/certs/files"
    
    if not os.path.exists(directorio_certificados):
        print("No hay certificados.")
        input("Presiona INTRO para volver al menú principal...")
        return  # Regresar al menú principal
    
    print("Mostrando todo el contenido en /opt/tak/certs/files:")
    # Listar todos los archivos en la carpeta
    certificados = os.listdir(directorio_certificados)
    
    if certificados:
        print("Archivos encontrados:")
        for certificado in certificados:
            print(certificado)
    else:
        print("No hay certificados existentes.")
    
    input("Presiona INTRO para volver al menú principal...")

def crear_certificados():
    print("Submenú - Crear Certificados")
    print("1. Crear Entidad Certificadora")
    print("2. Crear Certificados Genéricos")
    print("3. Atrás")
    opcion = input("Seleccione una opción: ")
    if opcion == "1":
        print("Creando certificado de Autoridad Certificadora...")
        ejecutar_comando("cd /opt/tak/certs && ./makeRootCa.sh")
        print("Certificado de Autoridad Certificadora creado correctamente.")
    elif opcion == "2":
        tipo_certificado = input("Defina el tipo de certificado (client/server): ")
        nombres_certificados = input("Introduzca el nombre del certificado(s) separados por comas: ")
        for nombre in nombres_certificados.split(","):
            ejecutar_comando(f"cd /opt/tak/certs && ./makeCert.sh {tipo_certificado} {nombre}")
        print("Certificados creados correctamente.")
    elif opcion == "3":
        return
    else:
        print("Opción inválida.")

def eliminar_certificados():
    certificado = input("Indique el nombre del certificado a eliminar (sin extensión): ").strip()
    # Definir las extensiones a eliminar
    extensiones = ['.csr', '.jks', '.key', '.p12', '.pem', '-trusted.pem']
    
    # Comprobar si alguno de los archivos existe en el directorio
    archivos_existentes = []
    for ext in extensiones:
        archivo = f"/opt/tak/certs/files/{certificado}{ext}"
        if os.path.isfile(archivo):
            archivos_existentes.append(archivo)
    
    if archivos_existentes:
        print("Certificados encontrados. Procediendo a eliminar...")
        for archivo in archivos_existentes:
            print(f"Eliminando archivo: {archivo}")
            os.remove(archivo)
        print("Certificados eliminados correctamente.")
    else:
        print(f"No se encontraron certificados para el nombre '{certificado}' en las extensiones especificadas.")

def gestionar_usuarios():
    print("Submenú - Gestión de Usuarios en Grupos")
    print("1. Agregar un certificado a un grupo")
    print("2. Desagregar un certificado de un grupo")
    print("3. Atrás")
    opcion = input("Seleccione una opción: ")
    if opcion == "1":
        certificado = input("Ingrese el nombre del certificado: ")
        if os.path.isfile(f"/opt/tak/certs/files/{certificado}.pem"):
            print("Certificado encontrado.")
            print("1. Grupo de Administración")
            print("2. Otros grupos")
            subopcion = input("Seleccione una opción: ")
            if subopcion == "1":
                ejecutar_comando(f"java -jar /opt/tak/utils/UserManager.jar certmod -A /opt/tak/certs/files/{certificado}.pem")
                print("Certificado agregado al grupo de Administración.")
            elif subopcion == "2":
                tipo_grupo = input("Indique el tipo de grupo (Entrada/Salida/Ambas): ")
                if tipo_grupo == "Entrada":
                    grupo = input("Indique el nombre del grupo: ")
                    ejecutar_comando(f"java -jar /opt/tak/utils/UserManager.jar certmod -ig{grupo} /opt/tak/certs/files/{certificado}.pem")
                elif tipo_grupo == "Salida":
                    grupo = input("Indique el nombre del grupo: ")
                    ejecutar_comando(f"java -jar /opt/tak/utils/UserManager.jar certmod -og{grupo} /opt/tak/certs/files/{certificado}.pem")
                elif tipo_grupo == "Ambas":
                    grupo = input("Indique el nombre del grupo: ")
                    ejecutar_comando(f"java -jar /opt/tak/utils/UserManager.jar certmod -g{grupo} /opt/tak/certs/files/{certificado}.pem")
            else:
                print("Opción inválida.")
        else:
            print("Certificado no encontrado.")
    elif opcion == "2":
        certificado = input("Ingrese el nombre del certificado: ")
        if os.path.isfile(f"/opt/tak/certs/files/{certificado}.pem"):
            ejecutar_comando(f"java -jar /opt/tak/utils/UserManager.jar certmod -r /opt/tak/certs/files/{certificado}.pem")
            print("Certificado eliminado del grupo.")
        else:
            print("Certificado no encontrado.")
    elif opcion == "3":
        return
    else:
        print("Opción inválida.")

def mostrar_urls():
    print("URLs de interés:")
    print("TAK Server Admin Tool: https://localhost:8443/Matri/metrics/index.html")
    print("Servidor Web TAK: https://localhost:8443/webtak/index.html")

def main():
    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ")
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
            print("Gracias, por usar nuestra aplicación. ¡Vuelve cuándo quieras!")
            break
        else:
            print("Opción inválida.")
        input("Presiona INTRO para continuar...")

if __name__ == "__main__":
    main()
