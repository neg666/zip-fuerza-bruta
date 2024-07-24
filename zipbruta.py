import sys
import subprocess

# Función para instalar dependencias
def install_dependencies():
    try:
        import zipfile
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "zipfile"])

install_dependencies()

import zipfile
import concurrent.futures

def ataque_fuerza_bruta(archivo, diccionario, password_length=None):
    found_password = None
    with zipfile.ZipFile(archivo, 'r') as zip_ref:
        for password in diccionario:
            if password_length and len(password) != password_length:
                continue
            try:
                zip_ref.extractall(pwd=password.encode('utf-8'))
                found_password = password
                break
            except (RuntimeError, zipfile.BadZipFile, zipfile.LargeZipFile):
                pass
    if found_password:
        return found_password

def main():
    archivo = input('Introduce la ruta del archivo protegido (ZIP): ')
    diccionario = input('Introduce la ruta del diccionario .txt: ')

    try:
        with open(diccionario, 'r', encoding='utf-8', errors='replace') as f:
            diccionario = f.read().splitlines()
    except FileNotFoundError:
        print('El diccionario no existe')
        return

    password_length = input('¿Deseas especificar una longitud de contraseña? (S/n): ')
    if password_length.lower() == 's':
        password_length = int(input('Especifica la longitud de la contraseña a probar: '))
    else:
        password_length = None

    num_threads = 20
    num_sections = num_threads

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for i in range(num_sections):
            section_start = i * len(diccionario) // num_sections
            section_end = (i + 1) * len(diccionario) // num_sections
            future = executor.submit(ataque_fuerza_bruta, archivo, diccionario[section_start:section_end], password_length)
            futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                print('Contraseña enco
