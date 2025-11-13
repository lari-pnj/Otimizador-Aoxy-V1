from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk
import time
from funcoes import *
try:
    from tktooltip import ToolTip
except Exception:
    class ToolTip:
        def __init__(self, widget, msg=None):
            # fallback quando tktooltip não estiver instalado
            return
import subprocess
import os, sys
from io import StringIO


def resource_path(relative_path):
    """Retorna o caminho correto, mesmo quando empacotado com PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# variável que guarda o último ponto de restauração criado
ultimo_ponto = None

# Exige que o app seja executado como Administrador: se não for, relança com UAC e encerra esta instância
def ensure_run_as_admin():
    try:
        import ctypes
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            is_admin = False
        if not is_admin:
            # monta argumentos a serem repassados
            extra_args = ''
            for a in sys.argv[1:]:
                # protege espaços
                extra_args += f' "{a}"'

            try:
                if getattr(sys, 'frozen', False):
                    # executável empacotado
                    ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, extra_args, None, 1)
                else:
                    script = os.path.abspath(__file__)
                    params = f'"{script}"' + extra_args
                    ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, params, None, 1)
            except Exception:
                print('Falha ao solicitar elevação via UAC.')
            sys.exit(0)
    except Exception:
        # se algo falhar, não bloqueia demais; seguirá sem elevação
        return

# chama no início
ensure_run_as_admin()

# Verifica se o app foi iniciado com a flag para criar ponto automaticamente (após elevação)
do_create_on_startup = False
if '--create-restore' in sys.argv:
    do_create_on_startup = True

def resource_path(relative_path):
    """Retorna caminho absoluto baseado no diretório do arquivo.

    Garante funcionamento tanto rodando como script quanto empacotado com PyInstaller.
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

#=============================================Funções-Locais================================================================

# Função para modificar a cor dos botões quando o mouse passa por cima "Hover Effect"-----
def add_hover_effect1(widget, 
    color_hover='#3a3a3a',
    color_normal='#3e3e4e'):
      def on_enter(e):
          widget['background']= color_hover
      def on_leave(e): 
          widget['background']= color_normal
      widget.bind("<Enter>", on_enter)
      widget.bind("<Leave>", on_leave)   
      
# Hover dos botoes de restauracao---------------------           
def add_hover_effect2(widget, 
    color_hover="#26486e",
    color_normal="#4a90e2"):
      def on_enter(e):
          widget['background']= color_hover
      def on_leave(e): 
          widget['background']= color_normal
      widget.bind("<Enter>", on_enter)
      widget.bind("<Leave>", on_leave)  
      
def add_hover_effect3(widget, 
    color_hover="#803f1f",
    color_normal="#e27d4a"):     
      def on_enter(e):
          widget['background']= color_hover
      def on_leave(e): 
          widget['background']= color_normal
      widget.bind("<Enter>", on_enter)
      widget.bind("<Leave>", on_leave)                  
      
      
# Função para criar um ponto de restauração-------------------------------------------------------------------

def criar_ponto_restauracao():
    global ultimo_ponto
    try:
        # Verifica se temos privilégios de administrador
        import ctypes
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            is_admin = False

        if not is_admin:
            atualizar_status("⚠️ É necessário executar o aplicativo como Administrador para criar um ponto de restauração.", cor="orange")
            # tenta relançar com elevação e sinalizar para criar o ponto automaticamente
            try:
                args = '"' + os.path.abspath(__file__) + '" --create-restore'
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, args, None, 1)
            except Exception:
                atualizar_status("❌ Falha ao solicitar elevação. Execute o app como Administrador manualmente.", cor="red")
            return
        # Tentativa: verificar e habilitar serviços necessários (srservice e VSS)
        atualizar_status("🔎 Verificando serviços necessários (srservice, VSS)...", cor="white")
        try:
            # Habilita e inicia srservice
            subprocess.run(["powershell", "-Command", "Set-Service -Name srservice -StartupType Automatic -ErrorAction SilentlyContinue"], check=False)
            subprocess.run(["powershell", "-Command", "Start-Service -Name srservice -ErrorAction SilentlyContinue"], check=False)
            # Habilita e inicia VSS (Volume Shadow Copy) como Manual
            subprocess.run(["powershell", "-Command", "Set-Service -Name VSS -StartupType Manual -ErrorAction SilentlyContinue"], check=False)
            subprocess.run(["powershell", "-Command", "Start-Service -Name VSS -ErrorAction SilentlyContinue"], check=False)
        except Exception as srv_e:
            atualizar_status(f"⚠️ Falha ao ajustar serviços: {srv_e}", cor="orange")

        # Verificar se System Protection está ativado na unidade C:
        atualizar_status("🔎 Verificando Proteção do Sistema na unidade C:\\...", cor="white")
        try:
            # Tenta habilitar a restauração para C:\ se ainda não estiver
            subprocess.run(["powershell", "-Command", "Enable-ComputerRestore -Drive 'C:\\'"], check=False)
        except Exception as en_e:
            atualizar_status(f"⚠️ Não foi possível habilitar Proteção do Sistema: {en_e}", cor="orange")

        # Agora tenta criar o ponto de restauração
        atualizar_status("⏳ Criando ponto de restauração...", cor="white")
        subprocess.run([
            "powershell",
            "-Command",
            "Checkpoint-Computer -Description 'Ponto_Otimizador_Aoxy' -RestorePointType 'MODIFY_SETTINGS'"
        ], check=True)
        # Após criar, obter o SequenceNumber (ID) do ponto recém-criado
        try:
            ps_cmd = "(Get-ComputerRestorePoint | Where-Object {$_.Description -eq 'Ponto_Otimizador_Aoxy'} | Sort-Object -Property CreationTime -Descending | Select-Object -First 1 -ExpandProperty SequenceNumber)"
            res = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True)
            seq = res.stdout.strip()
            if seq.isdigit():
                ultimo_ponto = int(seq)
                atualizar_status(f"💾 Ponto de restauração criado com sucesso! (ID: {ultimo_ponto})", cor="lightgreen")
            else:
                ultimo_ponto = None
                atualizar_status("⚠️ Ponto criado, mas não foi possível obter o ID do ponto.", cor="orange")
        except Exception as e_id:
            ultimo_ponto = None
            atualizar_status(f"⚠️ Ponto criado, mas falha ao obter ID: {e_id}", cor="orange")
    except Exception as e:
        atualizar_status(f"❌ Erro ao criar ponto de restauração: {e}", cor="red")
        
# Restaura ponto --------------------------------------------------------------------------------------------
        
def restaurar_ponto():
    if not ultimo_ponto:
        atualizar_status("⚠️ Nenhum ponto de restauração criado ainda!", cor="red")
        return

    # alerta o usuário que o PC será reiniciado
    if messagebox.askyesno("Restaurar Sistema", 
                           "Deseja realmente restaurar o sistema ao último ponto?\nO PC será reiniciado."):
        try:
            # Restore-Computer espera um ID numérico (SequenceNumber)
            subprocess.run([
                "powershell",
                "-Command",
                f"Restore-Computer -RestorePoint {ultimo_ponto}"
            ], check=True)
            atualizar_status("♻️ Restaurando para o ponto de restauração...", cor="yellow")
        except Exception as e:
            atualizar_status(f"❌ Erro ao restaurar ponto: {e}", cor="red")

#Função para atualizar status ----------------------------------------------------------------------------------

def atualizar_status(texto, cor='white'):
    historico_status.insert(END, texto)
    historico_status.itemconfig(tk.END, fg=cor)
    historico_status.yview(END)


def run_and_capture(func, *args, **kwargs):
    """Executa uma função, captura stdout/stderr e envia as linhas para o quadro de status."""
    old_out, old_err = sys.stdout, sys.stderr
    buf = StringIO()
    sys.stdout = buf
    sys.stderr = buf
    try:
        result = func(*args, **kwargs)
    except Exception as e:
        print(f"Erro ao executar {getattr(func, '__name__', str(func))}: {e}")
        result = None
    finally:
        sys.stdout = old_out
        sys.stderr = old_err
    output = buf.getvalue()
    if output:
        for line in output.splitlines():
            atualizar_status(line)
    return result
    
def executar_acao(texto, cor='white', tempo=2000):
    atualizar_status(texto, cor) 
    barra_progresso.start(10)
    janela.after(tempo, lambda: finalizar_acao("✅ Concluído!"))
      
def desativar_recursos():
    executar_acao('⚡desativando recursos...', cor='lightgreen', tempo=2000)
    run_and_capture(desativar_recursos_func)

def desinstalar_app():
    executar_acao('🗑️desinstalando app...', cor='yellow', tempo=2000)
    run_and_capture(desinstalar_app_func)

def atualizar_drives(): 
    executar_acao('🔄atualizando drives...', cor='lightblue', tempo=2000)
    run_and_capture(atualizar_drives_func)

def limpar_arquivos_desnecessarios(): # ABRIR COMO ADMIN # STATUS NA TELA DO APP
   executar_acao('🗑️excluindo arquivos...', cor='lightgray', tempo=2000)
   run_and_capture(limpar_arquivos_desnecessarios_func)

def recursos_energia(): 
    executar_acao('⚡ajustando recursos de energia...', cor='red', tempo=2000)
    run_and_capture(recursos_energia_func)

def limpar_cache_navegador(): # STATUS NA TELA DO APP
   executar_acao('🧹limpando cache...', cor='lightgreen', tempo=2000)
   run_and_capture(limpar_cache_navegador_func)

def desfragmentar_disco(): # ABRIR COMO ADMIN
   executar_acao('💽desfragmentando disco...', cor='lightgray', tempo=2000)
   run_and_capture(desfragmentar_disco_func)

def configuracoes_visuais():
    executar_acao('🎨configurando visual...', cor='orange', tempo=2000)
    run_and_capture(configuracoes_visuais_func)

def limpar_prefetch_temp(): # STATUS NA TELA
   executar_acao('🧹limpando prefetch/temp...', cor='blue', tempo=2000)
   run_and_capture(limpar_prefetch_temp_func)

def apps_inicializacao():
    executar_acao('🔄ajustando apps de inicializacao...', cor='purple', tempo=2000)
    run_and_capture(apps_inicializacao_func)
   
def monitorar_temperatura():
    executar_acao('🔍monitorando temperatura...', cor='lightblue', tempo=2000) 
    run_and_capture(monitorar_temperatura_func)


def finalizar_acao(texto):
    barra_progresso.stop()
    atualizar_status(texto, cor='lightgray')    

def Sair():
    if messagebox.askyesno('sair','Deseja realmente sair?'):
        janela.destroy()

#====================== Janela principal===========================================

janela = Tk()
janela.title('otimizador Aoxy v1.0')
janela.geometry('800x600')
janela.config(background="#1e1e2e")
janela.resizable(False, False)
try:
    janela.iconbitmap(resource_path("main/img/icon.ico"))
except Exception:
    # ignorar falha ao carregar ícone (arquivo pode não existir em ambiente de desenvolvimento)
    pass


# ======================Frame lateral==========================================

frame_menu = Frame(janela, bg='#2e2e3e', width=250)
frame_menu.pack(side='left', fill='y')

#criando os botoes do menu e tooltips

botoes = [
    ('⚡desativar recursos', desativar_recursos),
    ('🗑️desinstalar app', desinstalar_app),
    ('🔄atualizar drives', atualizar_drives),
    ('limpar arquivos desnecessarios', limpar_arquivos_desnecessarios),
    ('⚡recursos energia', recursos_energia),
    ('🧹limpar cache navegador', limpar_cache_navegador),
    ('💽desfragmentar disco', desfragmentar_disco),
    ('🎨configuracoes visuais', configuracoes_visuais),
    ('🧹limpar prefetch/temp', limpar_prefetch_temp),
    ('🔄apps de inicializacao', apps_inicializacao),
    ('🔍monitorar temperatura', monitorar_temperatura),
    ('❌Sair', Sair, '#a33')
]

# Mensagem para cada botão

Tooltips = [
    "Desativar recursos desnecessários pode tornar o sistema mais leve e rápido,\n\n ao impedir o carregamento de programas e serviços que você não usa.",
    "🗑️ Remove programas desnecessários instalados no PC.\n\n➜ Ajuda a liberar espaço e deixar o sistema mais limpo.",
    "🔄 Atualiza os drivers do computador.\n\n➜ Mantém os dispositivos funcionando corretamente e melhora a performance.",
    "🧹 Exclui arquivos temporários e inúteis.\n\n➜ Libera espaço em disco e pode deixar o PC mais rápido.",
    "⚡ Ajusta as configurações de energia.\n\n➜ Pode economizar bateria (notebooks) ou melhorar desempenho.",
    "🌐 Limpa o cache do navegador.\n\n➜ Libera espaço, melhora a velocidade da internet e resolve erros em sites.",
    "💽 Desfragmenta o disco rígido.\n\n➜ Organiza os arquivos no HD para aumentar a velocidade de leitura.",
    "🎨 Ajusta efeitos visuais do Windows.\n\n➜ Reduz o consumo de recursos e deixa o sistema mais leve.",
    "🧹 Remove arquivos do Prefetch e da pasta TEMP.\n\n➜ Elimina restos de programas antigos e acelera o sistema.",
    "🔄 Gerencia aplicativos que iniciam junto com o Windows.\n\n➜ Diminui o tempo de inicialização e economiza memória.",
    "🌡️ Monitora a temperatura do processador e do PC.\n\n➜ Ajuda a evitar superaquecimento e problemas de hardware.",
    "Fecha o programa" 
]
# Lista para armazenar cada botão
lista_botoes = []

# criando os botões e aplicando tooltip
for i, item in enumerate(botoes):
    if len(item) == 3:
        texto, command, cor = item
        bg_color = cor
    else:
        texto, command = item
        bg_color = '#3e3e4e'
    
    btn = tk.Button(
        frame_menu, text=texto, command=lambda c=command: c(), anchor='center', width=25,
        font=('Caviar Dreams', 10, 'bold'), bg=bg_color, fg='white',
        activebackground='#57576e', activeforeground='white',
        relief='flat', pady=10
    )
    btn.pack(fill='x', pady=2, padx=2)
    add_hover_effect1(widget=btn)
    
# adiciona tooltip correspondente
    ToolTip(btn, msg=Tooltips[i])
    
    # guarda botão na lista (se precisar depois)
    lista_botoes.append(btn)    
    
#======================Frame principal==========================================
frame_main = Frame(janela, bg='#1e1e2e')
frame_main.place(x=250, y=0, width=500, height=600)


notebook = ttk.Notebook(frame_main)
notebook.pack(fill="both", expand=True, padx=10, pady=10)    
    
#======================= aba de status =========================================

aba_status = tk.Frame(notebook, bg='#1b1b2f')
notebook.add(aba_status, text='status')

label_status = tk.Label(aba_status, text="📌 Histórico de Ações", font=("Heavitas", 14, "normal"),
                        bg="#1b1b2f", fg="lightblue", anchor="w")
label_status.pack(fill="x", padx=10, pady=(10,0))

historico_status = tk.Listbox(aba_status, bg="#2c2c44", fg="white",
                              font=("Caviar Dreams", 12, 'bold'), height=15, selectbackground="#57577e")
historico_status.pack(fill="both", expand=True, padx=10, pady=10)


# ================================ Aba Configurações =============================================
aba_config = tk.Frame(notebook, bg="#1b1b2f")
notebook.add(aba_config, text="Configurações")

tk.Label(aba_config, text="Configurações", font=("Heavitas", 14, "normal"),
         bg="#1b1b2f", fg="lightblue").pack(pady=20)

tk.Checkbutton(aba_config, text="Iniciar com Windows", bg="#1b1b2f", fg="white",
               font=("Caviar Dreams", 12, 'bold'), selectcolor="#2c2c44").pack(anchor="w", padx=20, pady=5)
tk.Checkbutton(aba_config, text="Notificações Ativas", bg="#1b1b2f", fg="white",
               font=("Caviar Dreams", 12 , 'bold'), selectcolor="#2c2c44").pack(anchor="w", padx=20, pady=5)


#====================================Aba ponto de restauração =================================
aba_restauracao = tk.Frame(notebook, bg="#1b1b2f")
notebook.add(aba_restauracao, text="Ponto de Restauração")

tk.Label(aba_restauracao, text="Ponto de Restauração do Sistema", font=("Heavitas", 14, "normal"),
         bg="#1b1b2f", fg="lightblue").pack(pady=20)
tk.Label(aba_restauracao, text="Crie um ponto de restauração\npara reverter alterações indesejadas.",
         font=("Caviar Dreams", 12, "bold"), bg="#1b1b2f", fg="white").pack(pady=10)

# Botoes de Restauração------
btn_criar_ponto = tk.Button(aba_restauracao, text='💾 Criar ponto de restauração', 
        command=criar_ponto_restauracao, font=('Caviar Dreams', 10, 'bold'),
        bg="#4a90e2", fg="white",
        activebackground="#357ab7", activeforeground="white",
        relief="raised", padx=20, pady=10 , width = 30
 ) 
btn_criar_ponto.pack(padx=5)
add_hover_effect2(btn_criar_ponto)

# Botão restaurar ponto de restauração
btn_restaurar_ponto = tk.Button(
    aba_restauracao, text="♻️ Voltar ao ponto de restauração",
    command=restaurar_ponto,
    font=('Caviar Dreams', 10, 'bold'),
    bg="#e27d4a", fg="white",
    activebackground="#b75c34", activeforeground="white",
    relief="raised", padx=20, pady=10 , width=30
)
btn_restaurar_ponto.pack(padx=5)
add_hover_effect3(btn_restaurar_ponto)

# ====================================Aba Sobre =============================================
aba_sobre = tk.Frame(notebook, bg="#1b1b2f")
notebook.add(aba_sobre, text="Sobre")

tk.Label(aba_sobre, text="Otimizador Aoxy v1.0", font=("Heavitas", 16, "normal"),
         bg="#1b1b2f", fg="lightblue").pack(pady=20)
tk.Label(aba_sobre, font=("Caviar Dreams", 12, "bold"), bg="#1b1b2f", fg="white").pack(pady=10)

sobre_path = resource_path(os.path.join('info', 'sobre.txt'))
try:
    with open(sobre_path, "r", encoding="utf-8") as f:
        conteudo_sobre = f.read()
except Exception:
    conteudo_sobre = "Arquivo 'sobre.txt' não encontrado.\nColoque-o na pasta 'info' ao lado do programa."
    
# Exibir o texto no widget
texto_sobre = tk.Text(aba_sobre, wrap="word", bg="#2c2c44", fg="white",
                      font=("Caviar Dreams", 11 , 'bold'), relief="flat", height=15)
texto_sobre.insert("1.0", conteudo_sobre)
texto_sobre.config(state="disabled") 
texto_sobre.pack(side="top", fill="x", padx=10, pady=10)    

#===================================================================================================

# Barra de progresso

barra_progresso = ttk.Progressbar(frame_main, orient="horizontal", length=350, mode="indeterminate")
barra_progresso.pack(pady=10)

# Rodapé
label_footer = tk.Label(
    janela, text="© 2025 Otimizador Aoxy",
    font=("Arial", 10), bg="#1e1e2e", fg="gray"
)
label_footer.pack(side="bottom", fill="x")

# Inicializa com mensagem de boas-vindas
atualizar_status("🎉 Bem-vindo ao Otimizador Aoxy!", cor ='lightgreen')

# Se o app foi iniciado com a flag para criar ponto automaticamente, agenda a ação após a interface carregar
if do_create_on_startup:
    janela.after(500, criar_ponto_restauracao)


mainloop()