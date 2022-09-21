import os
import platform
def limpiar_pantalla():
    os.system('cls') if platform.system() == "Windows" else
    os.system('clear')