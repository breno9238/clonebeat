#________IMPORTAÇÃO DE DEPENDÊNCIAS_________________________________________________________________
from screens.app import App         # Classe principal que gerencia as telas e o CustomTkinter

#________EXECUÇÃO DA APLICAÇÃO______________________________________________________________________
# Instanciação do Objeto Principal (Ponto de entrada do jogo)
clonebeat: App = App()

#________INICIALIZAÇÃO DO LOOP DE EVENTOS___________________________________________________________
# Mantém a interface gráfica ativa, processando cliques, teclas e renderização
clonebeat.mainloop()
