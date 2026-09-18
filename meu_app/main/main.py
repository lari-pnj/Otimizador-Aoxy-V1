from funcoes import *
import subprocess
import os
import time
import shutil
from itertools import zip_longest
import ctypes
import sys


# Solicita a permissao de administrador

#if not ctypes.windll.shell32.isUserAnAdmin():
#   ctypes.windll.shell32.shellExecuteW(
#      None, 'runas', sys.executable, ' '.join(sys.argv), None, 1
#   )
#   sys.exit()

   
def menu():
    
    titulo()

    # LISTA DE FUNÇÕES 1
    opcoes = ['[1] ➤  Desativar recursos',
             '[2] ➤  Desinstalar apps',
             '[3] ➤  Atualizar Drivers',
             '[4] ➤  Limpar Cache do Windows',
             '[5] ➤  Recursos De Energia',
             '[6] ➤  Configurações Visuais',
             '[7] ➤  Limpar Prefetch',
             '[8] ➤  Apps De Inicialização',
             '[9] ➤  Monitorar Temperatura',
             '[10] ➤  Desativar Apps de Segundo plano',
             '[11] ➤  Otimizar gamebar',
             '[12] ➤  Desativar Relatorios de erro',
             '[13] ➤  Desativar Cortana', 
             '[14] ➤  Aumentar prioridade da cpu/gpu', 
             '[15] ➤  Desativar telemetria' , 
             '[16] ➤  Aumentar Prioridade Foreground', 
             '[17] ➤  Melhorar Conexão de ping',
             '[18] ➤  EXIT']
    
    metade = len(opcoes)  // 2
    coluna1 = opcoes[:metade]
    coluna2 = opcoes[metade:]

    largura_col1 = 40
    largura_bloco = 75
    largura_terminal = shutil.get_terminal_size().columns
    margem_esquerda = max(0, (largura_terminal - largura_bloco) //2)
    espacos = " " * margem_esquerda

       
    for item1, item2 in zip_longest(coluna1, coluna2, fillvalue=""):
          print(f'{espacos}{item1:<{largura_col1}}{item2}')
          print()  


# titulo

def titulo():
   laranja = '\033[38;2;255;165;0m'
   reset ='\033[0m'
   titulo = "======== AOXY V1 ======="
   print('')
   print(f"{laranja}{titulo.center(shutil.get_terminal_size().columns)}{reset}") 
   print('\n')
   
#Função principal para escolha de opções

def main():
     while True:
        
        os.system('cls' if os.name =='nt' else 'clear')

        menu()

        escolha = input('Escolha Uma Opção: ')

        if escolha == '1':
            print('1- DESATIVAR RECURSOS')
            time.sleep(2)
            desativar_recursos_func()
            
        elif escolha == '2':
           print('2- DESINSTALAR APPS')
           time.sleep(2)
           desinstalar_app_func()
           
        elif escolha == '3':
           print('3- ATUALIZAR DRIVERS')
           time.sleep(2)
           atualizar_drives_func()
           
        elif escolha == '4':   
           print('4- LIMPAR CACHE DO WINDOWS')
           time.sleep(5)
           limpar_cache_windows_func()
           
        elif escolha == '5':   
           print('5- RECURSOS DE ENERGIA')
           time.sleep(2)
           recursos_energia_func()
           
        elif escolha == '6':
           print('7- CONFIGURAÇÕES VISUAIS')
           time.sleep(2)
           configuracoes_visuais_func()
           
        elif escolha == '7':
           print('8- LIMPAR PREFETCH')
           time.sleep(2)
           limpar_prefetch_temp_func()
           
        elif escolha == '8':
           print('9- APPS DE INICIALIZAÇÃO')
           time.sleep(2)
           apps_inicializacao_func()

        elif escolha == '9': 
          print('MONITORAR TEMPERATURA')
          time.sleep(2)
          monitorar_temperatura_func()

        elif escolha == '10':
          print('Desativar Apps de segundo plano') 
          time.sleep(2)   
          desativar_apps_seg_plan_func() 


# Função que altera o registro
        elif escolha == '11': 
            print('Otimizar gamebar')
            time.sleep(2)
            alterar_registros(winreg.HKEY_CURRENT_USER, r'System\GameConfigStore', 'GameDVR_Enabled', 0 )

        elif escolha == '12': 
            print('Desativar Relatorios de erro')
            time.sleep(2)
            desativar_relatorios_erro_func()

        elif escolha == '13': 
            print('Desativar Cortana')
            time.sleep(2)
            alterar_registros(
                      winreg.HKEY_LOCAL_MACHINE,
                      r'SOFTWARE\policies\microsoft\windows Search', 
                      'AllowCortana', 0,)

        elif escolha == '14': 
            print('Aumentar prioridade da cpu/gpu')
            time.sleep(2)
            alterar_registros(
                     winreg.HKEY_LOCAL_MACHINE,
                     r'SYSTEM\CurrentControlSet\Control\PriorityControl',
                     'Win32PrioritySeparation',
                     38,)
   
        elif escolha == '15': 
            print('Desativar telemetria')
            time.sleep(2)
            desativar_telemetria_func()

        elif escolha == '16': 
            print('Aumentar Prioridade Foreground')
            time.sleep(2)
            aumentar_foreground_func()

        elif escolha == '17': 
            print('Melhorar Conexão de ping')
            time.sleep(2)
            melhorar_ping_func('1.1.1.1')  

        elif escolha == '18':
           print('saindo.....')  
           break                                                                    
                       
        else:
          break

if __name__ == '__main__':
   main()  
        

