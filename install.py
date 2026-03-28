import os
import sys
import subprocess

def run_command(command):
    subprocess.call(command, shell=True)

print("🚀 Iniciando instalação do Fernando IA...")
run_command("pip install -r requirements.txt")
print("✅ Instalação concluída com sucesso!")
