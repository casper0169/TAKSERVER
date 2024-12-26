import os
import subprocess
import socket
import time

# Variables para controlar las opciones deshabilitadas
opcion_1_habilitada = True
opcion_2_habilitada = True
opcion_3_habilitada = True

def mostrar_menu_principal():
    os.system('clear')
    print("====================================")
    print("       MENÚ PRINCIPAL - SERVIDOR TAK")
    print("====================================")
    
    if not opcion_1_habilitada:
        print("\033[9m1. Instalación del Servidor TAK\033[0m")
    else:
        print("1. Instalación del Servidor TAK")
    
    if not opcion_2_habilitada:
        print("\033[9m2. Definir dirección IPv4 privada estática\033[0m")
    else:
        print("2. Definir dirección IPv4 privada estática")
    
    if not opcion_3_habilitada:
        print("\033[9m3. Definir los puertos del Firewall\033[0m")
    else:
        print("3. Definir los puertos del Firewall")
        
    print("4. Mostrar certificados existentes")
    print("5. Crear certificados")
    print("6. Eliminar certificados")
    print("7. Gestión de usuarios en grupos")
    print("8. URLs de interés")
    print("9. Salir")
    print("====================================")

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
    global opcion_1_habilitada
    print("Instalando Servidor TAK automáticamente...")

    comandos = [
        "sudo apt update && apt full-upgrade -y",
        "echo '* soft nofile 32768\n* hard nofile 32768' | sudo tee -a /etc/security/limits.conf > /dev/null",
        "sudo mkdir -p /etc/apt/keyrings",
        "sudo curl https://www.postgresql.org/media/keys/ACCC4CF8.asc --output /etc/apt/keyrings/postgresql.asc",
        "sudo sh -c 'echo \"deb [signed-by=/etc/apt/keyrings/postgresql.asc] http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main\" > /etc/apt/sources.list.d/postgresql.list'",
        "sudo apt install -y openjdk-17-jdk",
        "sudo add-apt-repository ppa:openjdk-r/ppa -y",
        "sudo apt update && sudo apt full-upgrade -y",
        "sudo update-alternatives --config java",
        "sudo apt install -y maven gradle"
    ]
    
    for comando in comandos:
        print(f"Ejecutando: {comando}")
        ejecutar_comando(comando)  # Ejecuta y muestra la salida de cada comando
        time.sleep(2)  # Pausa entre comandos para que el proceso sea más claro para el usuario

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
    archivo_metadata = "/opt/tak/certs/cert-metadata.sh"
    print(f"Editando {archivo_metadata} automáticamente...")
    try:
        with open(archivo_metadata, 'a') as file:
            file.write("\n# Configuración automática añadida por el script\n")
    except Exception as e:
        print(f"Error al editar {archivo_metadata}: {e}")
    print(f"Abriendo {archivo_metadata} para su edición...")
    os.system(f"sudo nano {archivo_metadata}")
    print("¡Enhorabuena! El Servidor TAK se instaló correctamente.")
    
    # Deshabilitar la opción 1 después de la ejecución exitosa
    opcion_1_habilitada = False

def configurar_ipv4_estatica():
    global opcion_2_habilitada
    print("Configura la dirección IPv4 privada estática en /etc/netplan/00-installer-config.yaml.")
    print("Ejemplo de configuración:\n"
          "network:\n"
          "  version: 2\n"
          "  renderer: NetworkManager\n"
          "  ethernets:\n"
          "    eth0:\n"
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
    print("¡Enhorabuena! Configuración de red completada.")
    
    # Deshabilitar la opción 2 después de la ejecución exitosa
    opcion_2_habilitada = False

def configurar_firewall():
    global opcion_3_habilitada
    print("Configurando el Firewall...")
    ejecutar_comando("sudo apt-get install -y ufw")
    ejecutar_comando("sudo ufw enable")
    ejecutar_comando("sudo ufw allow 8089/tcp")
    ejecutar_comando("sudo ufw allow 8443/tcp")
    ejecutar_comando("sudo ufw status verbose")
    ejecutar_comando("sudo ufw reload")
    print("¡Enhorabuena! Puertos configurados correctamente.")
    
    # Deshabilitar la opción 3 después de la ejecución exitosa
    opcion_3_habilitada = False

def mostrar_certificados():
    print("Mostrando todo el contenido en /opt/tak/certs/files:")
    # Listar todos los archivos en la carpeta
    certificados = os.listdir("/opt/tak/certs/files")
    
    if certificados:
        print("Archivos encontrados:")
        for certificado in certificados:
            print(certificado)
    else:
        print("No se encontraron archivos en el directorio.")
    
    print("\nPresiona ENTER para regresar al menú principal.")
    input()  # Espera hasta que el usuario presione ENTER

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
        print(f"No se encontraron certificados para el nombre '{certificado}'.")

def gestionar_usuarios():
    print("Submenú - Gestión de Usuarios en Grupos")
    print("1. Añadir usuario a grupo")
    print("2. Eliminar usuario de grupo")
    print("3. Atrás")
    opcion = input("Seleccione una opción: ")
    if opcion == "1":
        usuario = input("Nombre del usuario: ").strip()
        grupo = input("Nombre del grupo: ").strip()
        ejecutar_comando(f"sudo usermod -aG {grupo} {usuario}")
        print(f"Usuario {usuario} añadido al grupo {grupo}.")
    elif opcion == "2":
        usuario = input("Nombre del usuario: ").strip()
        grupo = input("Nombre del grupo: ").strip()
        ejecutar_comando(f"sudo deluser {usuario} {grupo}")
        print(f"Usuario {usuario} eliminado del grupo {grupo}.")
    elif opcion == "3":
        return
    else:
        print("Opción inválida.")

def mostrar_urls():
    print("URLs de interés relacionadas con el Servidor TAK:")
    print("1. Administración por WebTak: https://localhost:8443/webtak/index.html")
    print("2. Administración por Metrics Dashboards: https://localhost:8443/Matri/metrics/index.html#!")
    print("3. Atrás")
    opcion = input("Seleccione una opción: ")
    if opcion == "3":
        return
    else:
        print("Opción inválida.")

def main():
    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ")

        if opcion == "1" and opcion_1_habilitada:
            instalar_tak()
        elif opcion == "2" and opcion_2_habilitada:
            configurar_ipv4_estatica()
        elif opcion == "3" and opcion_3_habilitada:
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
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")
        time.sleep(1)

if __name__ == "__main__":
    main()
