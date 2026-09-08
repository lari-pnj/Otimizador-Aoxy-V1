import utils, options
      
LOGO = "\n".join([
    "=" * 50,
    " Otimizador AOXY ".center(50, "-"),
    "=" * 50
])   

def main():
   print('\033c') # ANSI de limpar o terminal (faz a mesma coisa do clean/cls, só roda uma vez pq é pesado e pode bugar se usar muitas vezes rápido)

   try:
      while True:
         utils.clean()
         
         print(LOGO)
         
         options.showOptions()
         options.handleOption()
   except:
      return

if __name__ == '__main__':
   main()  