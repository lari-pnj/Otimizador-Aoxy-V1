import os
import subprocess
import shutil
import winreg
import time

# função 1
def desativar_recursos_func():
     os.startfile(r"C:\Windows\System32\OptionalFeatures.exe")
     
# função 2
def desinstalar_app_func():
     subprocess.run('appwiz.cpl', shell = True)
     
# função 3
def atualizar_drives_func():
     os.startfile("devmgmt.msc")

# função 4
def limpar_cache_windows_func():
     # Pastas a limpar
     pastas = [r"C:\Windows\Temp",# Pasta Temp do sistema
     os.environ.get('TEMP')# Pasta Temp do usuário (%Temp%)
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


# função 5
def recursos_energia_func():
     subprocess.run('powercfg.cpl', shell = True)

  
# função 6
def configuracoes_visuais_func():
      # Usa caminho absoluto para evitar dependência do PATH
      systemroot = os.environ.get('SystemRoot', r'C:\Windows')
      exe = os.path.join(systemroot, 'System32', 'SystemPropertiesPerformance.exe')
      try:
           subprocess.run([exe], check=False)
      except Exception:
           # fallback: tentar chamar apenas pelo nome (em alguns sistemas funciona)
           subprocess.run("SystemPropertiesPerformance.exe", shell=True)


# função 7
#def limpar_prefetch_temp_func():
#     prefetch_path = r"C:\Windows\Prefetch"

     # Verifica se a pasta existe 
#     if os.path.exists(prefetch_path):
#          for file in os.listdir(prefetch_path):
#               file_path = os.path.join(prefetch_path, file)
#               try:
#                    if os.path.isfile(file_path):
#                         os.remove(file_path)  # Apaga arquivos
#                         print(f"Apagado: {file_path}")
#               except PermissionError:
#                    print(f"Sem permissão para apagar: {file_path}")
#                    time.sleep(2)
#               except Exception as e:
#                    print(f"Erro ao apagar {file_path}: {e}")
#                    time.sleep(2)
#          else:
#           print("Pasta Prefetch não encontrada.")


# função 8
def apps_inicializacao_func(): 
    subprocess.run("taskmgr", shell=True)
    
# função 9
def monitorar_temperatura_func():
     subprocess.run("resmon.exe", shell=True)



################################################# FUNÇÕES A SEREM ENCREMENTADAS ##############################################

# função 10
def desativar_apps_seg_plan_func(): 
     path = (
           r'Software\Microsoft\Windows\CurrentVersion\BackgroundAcessAplications'
      )
     try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, path)
        winreg.SetValueEx(key, "GlobalUserDisabled", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        print('[Sucesso] Apps em segundo plano desativados.')
        time.sleep(2)
     except Exception as e:
        print(f'[Erro] Apps segundo plano {e}')  
        time.sleep(2) 


# função 11 (revisar)
#def desativar_relatorios_erro_func():
 #    path = (
 #         r'SOFTWARE\Microsoft\Windows\Windows Error Reporting'        
 #    )
 #    try:
 #        key = winreg.Createkey(winreg.HKEY_LOCAL_MACHINE, path)
 #        winreg.SetValueEx(key, "disable", 0, winreg.REG_DWORD, 1)
 #        winreg.CloseKey(key)
 #    except Exception as e:
 #         print(f'[Erro Registro WER]: {e}')
 #         time.sleep(2)

 #   subprocess.run('net stop WerSvc', shell=True, capture_output=True)
 #    subprocess.run(
 #         'sc config WerSvc start= disable', shell=True, capture_output=True
 #    )     
 #    print('[Sucesso] Relatórios de erro desativados.') 
 #    time.sleep(2)   



# FUNÇÕES QUE ALTERAM OS REGISTROS #############################################

def alterar_registros(hive, path, nome_valor, valor, tipo=winreg.REG_DWORD):
     try:
        key = winreg.CreateKey(hive, path)
        winreg.SetValueEx(key, nome_valor, 0, tipo, valor)
        winreg.CloseKey(key)
        print(f'[Sucesso] Chave alterada: {nome_valor}')
     except Exception as e:
          print(f'[Erro] Falha ao alterar {nome_valor}: {e}')


# função 12
# Desativar Cortana
#     alterar_registros(
#          winreg.HKEY_LOCAL_MACHINE,
#          r'SOFTWARE\policies\microsoft\windows Search', 
#          'AllowCortana', 0,)

# função 13    
# Otimizar gamebar
#     alterar_registros(
#          winreg.HKEY_CURRENT_USER, r'System\GameConfigStore', 'GameDVR_Enabled', 0 )

# função 14     
# Aumentar prioridade da cpu/gpu
#     alterar_registros(
#          winreg.HKEY_LOCAL_MACHINE,
#          r'SYSTEM\CurrentControlSet\Control\PriorityControl',
#          'Win32PrioritySeparation', 38,)


# função 15
def desativar_telemetria_func():
     path = r'SOFTWARE\Policies\Microsoft\windows\DataCollection'
     try:
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, path)
        winreg.SetValueEx(key, 'AllowTelemetry', 0, winreg.REG_DWORD, 0)
        winreg.Closekey(key)
     except Exception as e:
          print('[Sucesso] Telemetria desativada.')
          time.sleep(2)   


# função 16
def aumentar_foreground_func():
     path = r'SYSTEM\CurrentControlSet\Control\PriorityControl'
     try:
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, path)
        winreg.SetValueEx(
             key, "Win32PrioritySeparation", 0, winreg.REG_DWORD, 38
        ) 
        winreg.CloseKey(key)
        print("[Sucesso] Prioridades Foreground aumentada.")
        time.sleep(2)
     except Exception as e:
          print(f"[Erro prioridade foreground]: {e}")   
          time.sleep(2)


# função 17
# 9- Melhorar Conexão de ping (Dns jumper)
#def melhorar_ping_func(ip_dns='1.1.1.1'):
#cmd = ('powershell -Command "Get-NetAdapter | where-Object {$_.Status -eq \'up\'}'
#     f" | Set-DnsClientServerAddress -ServerAddresses ('{ip_dns}')\"")
#executar_comando(cmd)
#print(f'[Rede] DNS alterado para {ip_dns}')

#melhorar_ping_func('1.1.1.1')