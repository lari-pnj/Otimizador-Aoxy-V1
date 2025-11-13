import os
import subprocess
import psutil
import shutil
import tempfile


# Desativar recursos desnecessários pode tornar o sistema mais leve e rápido===================================

def desativar_recursos_func():
     os.startfile(r"C:\Windows\System32\OptionalFeatures.exe")
     

# Abre os programas instalados no pc
def desinstalar_app_func():
     subprocess.run('appwiz.cpl', shell = True)
     

# Verificar drives a serem atualizados
def atualizar_drives_func():
     os.startfile("devmgmt.msc")


# Função para limpar pastas com arquivos desnecessarios

def limpar_arquivos_desnecessarios_func():
     # Pastas a limpar
     pastas = [
     r"C:\Windows\Temp",      # Pasta Temp do sistema
     os.environ.get('TEMP')   # Pasta Temp do usuário (%Temp%)
     ]
     for pasta in pastas:
          if os.path.exists(pasta):
               for item in os.listdir(pasta):
                    item_path = os.path.join(pasta, item)
                    try:
                         if os.path.isfile(item_path) or os.path.islink(item_path):
                              os.remove(item_path)  # Apaga arquivos
                         elif os.path.isdir(item_path):
                              shutil.rmtree(item_path)  # Apaga pastas
                         print(f"Apagado: {item_path}")
                    except PermissionError:
                         print(f"Sem permissão para apagar: {item_path}")
                    except Exception as e:
                         print(f"Erro ao apagar {item_path}: {e}")
          else:
               print(f"Pasta não encontrada: {pasta}")


# Abre a janela de Opções de Energia
def recursos_energia_func():
     subprocess.run('powercfg.cpl', shell = True)


# Limpar o cache do navegador CHROME
def limpar_cache_navegador_func():
     chrome_cache = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache")
     limpar_arquivos_desnecessarios_func(chrome_cache)
     print("Cache do Chrome limpo!")
     
# Desfragmentar a unidade C: necessario só para hd:
def desfragmentar_disco_func():
     subprocess.run("defrag C: /O", shell=True)
     
     
# Abrir Configurações Avançadas de Desempenho (Efeitos Visuais)
def configuracoes_visuais_func():
      # Usa caminho absoluto para evitar dependência do PATH
      systemroot = os.environ.get('SystemRoot', r'C:\Windows')
      exe = os.path.join(systemroot, 'System32', 'SystemPropertiesPerformance.exe')
      try:
           subprocess.run([exe], check=False)
      except Exception:
           # fallback: tentar chamar apenas pelo nome (em alguns sistemas funciona)
           subprocess.run("SystemPropertiesPerformance.exe", shell=True)

# DELETA A PASTA PREFETCH

def limpar_prefetch_temp_func():
# Caminho da pasta Prefetch
     prefetch_path = r"C:\Windows\Prefetch"

     # Verifica se a pasta existe
     if os.path.exists(prefetch_path):
     # Lista os arquivos
          for file in os.listdir(prefetch_path):
               file_path = os.path.join(prefetch_path, file)
               try:
                    if os.path.isfile(file_path):
                         os.remove(file_path)  # Apaga arquivos
                         print(f"Apagado: {file_path}")
               except PermissionError:
                    print(f"Sem permissão para apagar: {file_path}")
               except Exception as e:
                    print(f"Erro ao apagar {file_path}: {e}")
          else:
           print("Pasta Prefetch não encontrada.")


# Abre a pasta de inicialização do usuário

def apps_inicializacao_func(): 
    subprocess.run("taskmgr", shell=True)
    
# Abre o monitor de recursos para monitorar a temperatura
def monitorar_temperatura_func():
     subprocess.run("resmon.exe", shell=True)

#Recursos futuros-------------------------------------------------------------------------------------------------------
    
     
#Liberar cache do DNS (pode acelerar internet às vezes)  
# def limpar_cache_dns():
#      subprocess.run('ipconfig /flushdns', shell = True) 
     
# resultado = subprocess.run("ipconfig /flushdns", shell=True, capture_output=True, text=True)

# print("Saída:")
# print(resultado.stdout)
# print("Erros:")
# print(resultado.stderr)  
    