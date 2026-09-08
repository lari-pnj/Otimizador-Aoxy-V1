import models, sys, utils, os

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
   for i, opt in enumerate(OPTIONS):
      alignment = "0" if i < 9 else ""
      number    = alignment + str(i + 1)
      
      print(f"[{number}] ➤ ", opt.name)
      
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
   