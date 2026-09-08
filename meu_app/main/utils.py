import os, shutil

def clean():
   print("\033[H\033[J") # ANSI de mover o cursor pro primeiro caractere do terminal e limpar a tela (mais limpo que clean/cls)

def open_system_program(path: str): # Função genérica pra abrir arquivo pela path
    try:
        os.startfile(path)
    except Exception as e:
        print(f"Erro ao abrir {path}: {e}")
        
        
def clear_multi_dir(paths: list[tuple]): # Função genérica para limpar vários diretórios
    for path, delete_child in paths:
        if path:
            clear_dir(path, delete_child)
        else:
            print("[Erro] Caminho não definido (Variável de ambiente ausente).")
        
def clear_dir(path: str, delete_child=True): # Função genérica para deletar/limpar um diretório
    if not os.path.exists(path):
        print(f"Pasta não encontrada: {path}")
        return
    
    print(f"Limpando: {path}")
    
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
                print(f"  [Arquivo] Apagado: {item}")
                
            elif os.path.isdir(item_path) and delete_child:
                shutil.rmtree(item_path)
                
                print(f"  [Pasta] Apagada: {item}")
                
        except PermissionError:
            print(f"  [Erro] Sem permissão: {item}")
            
        except Exception as e:
            print(f"  [Erro] Falha ao apagar {item}: {e}")