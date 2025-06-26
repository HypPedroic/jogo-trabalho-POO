import pygame
import sys
from managers.game_manager import GameManager
from managers.state_manager import GameState
import os
import json

class Jogo:
    def __init__(self):
        print("Inicializando pygame...")
        pygame.init()
        print("Pygame inicializado!")
        
        # Configuração da janela
        self.__screen = pygame.display.set_mode((832, 640))
        pygame.display.set_caption("ReaperQuest 💀")
        
        # Inicializa o gerenciador do jogo
        self.__game_manager = GameManager(self.__screen)

    def run(self):
        """Loop principal do jogo"""
        try:
            while self.__game_manager.running:
                # Processa eventos
                self.__game_manager.processar_eventos()
                
                # Atualiza o estado do jogo
                if self.__game_manager.estado == "menu":
                    print("Executando menu...")
                    self.__game_manager.menu.running = True
                    nome = self.__game_manager.menu.run()
                    print(f"Menu retornou: {nome}")
                    
                    if nome == "continuar":
                        print("Carregando progresso salvo...")
                        self.__game_manager.iniciar_jogo_carregado()
                    elif isinstance(nome, dict):  # Se retornou um dicionário, inicia o jogo normalmente
                        print(f"Iniciando jogo com jogador: {nome}")
                        try:
                            save_path = "data/save.json"
                            if os.path.exists(save_path):
                                with open(save_path, "r", encoding="utf-8") as f:
                                    progresso = json.load(f)
                                if progresso.get("nome") == nome["nome"]:
                                    os.remove(save_path)
                        except Exception:
                            pass
                        self.__game_manager.iniciar_jogo(nome)
                    elif not self.__game_manager.menu.running:  # Se o menu foi fechado
                        print("Menu foi fechado, encerrando jogo")
                        break
                    else:
                        print("Menu continua rodando...")
                        
                elif self.__game_manager.estado == "jogando":
                    self.__game_manager.update()
                    
                elif self.__game_manager.estado == "game_over":
                    print("Executando menu de game over...")
                    self.__game_manager.menu.running = True
                    self.__game_manager.menu.run()
                    
                    if not self.__game_manager.menu.running:  # Se o menu foi fechado
                        print("Menu de game over foi fechado")
                        if self.__game_manager.menu.estado == "menu_principal":
                            self.__game_manager.estado = "menu"
                            print("Voltando ao menu principal")
                        else:
                            break
                            
                elif self.__game_manager.estado == "vitoria":
                    print("Executando tela de vitória...")
                    self.__game_manager.menu.running = True
                    self.__game_manager.menu.run()
                    
                    if not self.__game_manager.menu.running:  # Se o menu foi fechado
                        print("Tela de vitória foi fechada")
                        if self.__game_manager.menu.estado == "menu_principal":
                            self.__game_manager.estado = "menu"
                            print("Voltando ao menu principal")
                        else:
                            break
                
                # Atualiza a tela
                pygame.display.flip()
                self.__game_manager.clock.tick(60)
                
        except Exception as e:
            print(f"Erro durante execução do jogo: {e}")
            import traceback
            traceback.print_exc()
        finally:
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    print("Iniciando o jogo...")
    try:
        jogo = Jogo()
        print("Jogo criado com sucesso!")
        jogo.run()
        print("Jogo finalizado.")
    except Exception as e:
        print(f"Erro ao inicializar o jogo: {e}")
        import traceback
        traceback.print_exc()
