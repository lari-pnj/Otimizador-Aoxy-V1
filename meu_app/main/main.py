import utils, options, shutil
      
LOGO = "\n".join([
    "\033[38;2;255;165;0m" +
    "======== AOXY V1 =======".center(shutil.get_terminal_size().columns) + 
    '\033[0m\n'
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