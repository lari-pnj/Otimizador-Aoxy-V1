import models, sys, utils, os, shutil
from itertools import zip_longest

OPTIONS = (
    models.Option("Desativar Recursos",             
                    lambda: utils.open_system_program('OptionalFeatures.exe')),

    models.Option("Desinstalar apps",               
                    lambda: utils.open_system_program('appwiz.cpl')),

    models.Option("Atualizar Drivers",              
                    lambda: utils.open_system_program('devmgmt.msc')),

    models.Option("Limpar Arquivos Desnecessarios", 
                    lambda: utils.clear_multi_dir([
                        (os.environ.get('TEMP'), True),
                        (r"C:\Windows\Temp",     True),
                 ])
    ),

    models.Option("Recursos De Energia",            
                    lambda: utils.open_system_program('powercfg.cpl')
    ),

    models.Option("Configurações Visuais",          
                    lambda: utils.open_system_program('SystemPropertiesPerformance.exe')
    ),

    models.Option("Limpar Prefetch",                
                    lambda: utils.clear_dir(r"C:\Windows\Prefetch", False)
    ),

    models.Option("Apps De Inicialização",          
                    lambda: utils.open_system_program('taskmgr')            
    ),

    models.Option("Monitorar Temperatura",          
                    lambda: utils.open_system_program('resmon')
    ),

    models.Option("Sair",                           
                    sys.exit
    ),
)


def showOptions():
    half    = (len(OPTIONS) + 1) // 2
    coluna1 = OPTIONS[:half]
    coluna2 = OPTIONS[half:]

    widthCol1    = 40
    widthBlock   = 75

    termWidth  = shutil.get_terminal_size().columns
    leftMargin = max(0, (termWidth - widthBlock) // 2)
    spaces     = " " * leftMargin

    print('') # \n

    for opt1, opt2 in zip_longest(coluna1, coluna2, fillvalue=None):
        line1 = ""
        line2 = ""

        if opt1 is not None:
            i = OPTIONS.index(opt1)
            number = f"{i + 1:02}"
            line1 = f"[{number}] ➤ {opt1.name}"

        if opt2 is not None:
            i = OPTIONS.index(opt2)
            number = f"{i + 1:02}"
            line2 = f"[{number}] ➤ {opt2.name}"

        print(f"{spaces}{line1:<{widthCol1}}{line2}\n")

    print()
   
def handleOption():
   while True:
      choice = input('Escolha Uma Opção: ')
      
      try:
         idx = int(choice)
         
         if 1 <= idx <= len(OPTIONS):
            choice = idx - 1 
            break
         else:
            print('Opção Inválida! Escolha um número entre 1 e', len(OPTIONS))
            
      except ValueError:
         print('Erro: Por favor, digite apenas números.')
         
   print(f"Você escolheu {OPTIONS[choice].name.lower()}")
   OPTIONS[choice].handler()
   